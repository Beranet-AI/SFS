#!/usr/bin/env python3
"""
Data Flow Analyzer - تحلیل دقیق جریان داده در سیستم SFS
"""

import os
import ast
import re
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow, FancyArrowPatch
import matplotlib.patheffects as path_effects
import numpy as np
import warnings

class DataFlowAnalyzer:
    def __init__(self, project_root, scan_dirs=None):
        self.project_root = Path(project_root)
        # مسیرهای مشخص شده برای اسکن
        if scan_dirs:
            self.scan_dirs = scan_dirs
        else:
            # مسیرهای پیش‌فرض
            self.scan_dirs = ['sfs/backend', 'sfs/frontend']
        
        self.graph = nx.DiGraph()
        self.data_flows = defaultdict(list)
        self.modules_info = {}
        self.function_calls = defaultdict(list)
        self.input_points = []
        self.output_points = []
        self.module_io = defaultdict(dict)  # ورودی/خروجی هر ماژول
        
    def scan_project(self):
        """اسکن پروژه و استخراج جریان داده"""
        print(f"🔍 در حال اسکن پروژه: {self.project_root}")
        print(f"📁 مسیرهای اسکن: {', '.join(self.scan_dirs)}")
        
        python_files = []
        
        # اسکن فقط در مسیرهای مشخص شده
        for scan_dir in self.scan_dirs:
            scan_path = self.project_root / scan_dir
            if not scan_path.exists():
                print(f"  ⚠️ مسیر {scan_dir} وجود ندارد، رد کردن...")
                continue
                
            print(f"  📂 اسکن مسیر: {scan_dir}")
            dir_files = list(scan_path.rglob("*.py"))
            python_files.extend(dir_files)
            print(f"    یافت شد: {len(dir_files)} فایل پایتون")
        
        print(f"📁 کل فایل‌های پایتون برای تحلیل: {len(python_files)}")
        
        # محدود کردن تعداد فایل‌ها برای جلوگیری از Overload
        if len(python_files) > 150:
            print(f"  ⚠️ تعداد فایل‌ها زیاد است ({len(python_files)}). فقط ۱۵۰ فایل اول تحلیل می‌شوند.")
            python_files = python_files[:150]
        
        # فیلتر فایل‌های مشکوک
        filtered_files = []
        for py_file in python_files:
            if any(x in str(py_file) for x in ['venv', '__pycache__', '.env', '.git', '.tox', 'node_modules', 'migrations']):
                continue
            
            # فایل‌های خاص که ممکن است پایتون معتبر نباشند
            file_name = py_file.name.lower()
            if any(x in file_name for x in ['open-postgres', 'setup', 'install', 'activate', 'deactivate']):
                continue
            
            filtered_files.append(py_file)
        
        print(f"📊 فایل‌های فیلتر شده برای تحلیل: {len(filtered_files)}")
        
        for py_file in filtered_files:
            self.analyze_file(py_file)
        
        print(f"📊 ماژول‌های تحلیل شده: {len(self.modules_info)}")
        
        # تحلیل جریان داده
        self.analyze_data_flows()
        
        if not self.modules_info:
            print("⚠️ هیچ ماژول معتبری یافت نشد! خروجی‌ها تولید نمی‌شوند.")
            return None
        
        return self.generate_flowcharts()
    
    def analyze_file(self, file_path):
        """تحلیل یک فایل و استخراج اطلاعات جریان داده"""
        try:
            # محاسبه مسیر نسبی
            try:
                relative_path = file_path.relative_to(self.project_root)
            except ValueError:
                relative_path = Path(file_path.name)
                
            module_name = str(relative_path).replace('.py', '').replace('/', '.').replace('\\', '.')
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # بررسی سینتکس
            try:
                tree = ast.parse(content)
            except SyntaxError:
                return
            
            self.graph.add_node(module_name, 
                              type='module',
                              path=str(relative_path),
                              size=os.path.getsize(file_path))
            
            # استخراج importها و توابع
            imports, functions, classes, api_endpoints = self.extract_file_info(tree, module_name)
            
            # ذخیره اطلاعات ماژول
            self.modules_info[module_name] = {
                'imports': imports,
                'functions': functions,
                'classes': classes,
                'api_endpoints': api_endpoints,
                'num_functions': len(functions),
                'num_classes': len(classes),
                'num_endpoints': len(api_endpoints)
            }
            
            # شناسایی نقاط ورودی (API endpoints, main functions)
            if api_endpoints:
                self.input_points.extend([(module_name, ep) for ep in api_endpoints])
            elif 'main' in module_name.lower() or 'app' in module_name.lower():
                self.input_points.append((module_name, 'main'))
            
            # شناسایی نقاط خروجی (functions that return data)
            for func_name, func_info in functions.items():
                if any(keyword in func_name.lower() for keyword in ['get_', 'fetch_', 'retrieve_', 'return_', 'create_', 'save_']):
                    self.output_points.append((module_name, func_name))
            
            # اضافه کردن importها به گراف
            for imp in imports:
                if imp and len(imp) > 0:
                    self.graph.add_edge(module_name, imp, 
                                      type='import',
                                      weight=1)
                    self.data_flows[module_name].append({
                        'target': imp,
                        'type': 'import',
                        'description': f"Import ماژول {imp}"
                    })
            
        except Exception as e:
            print(f"  ⚠️ خطا در تحلیل {file_path.name}: {e}")
    
    def extract_file_info(self, tree, module_name):
        """استخراج اطلاعات دقیق از فایل"""
        imports = []
        functions = {}
        classes = {}
        api_endpoints = []
        
        for node in ast.walk(tree):
            # استخراج importها
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name:
                        imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
            
            # استخراج توابع
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                params = [arg.arg for arg in node.args.args]
                returns = self.detect_return_type(node)
                
                functions[func_name] = {
                    'params': params,
                    'returns': returns,
                    'docstring': ast.get_docstring(node) or '',
                    'has_return': self.has_return_statement(node)
                }
                
                # شناسایی API endpoints
                if any(decorator for decorator in node.decorator_list 
                      if isinstance(decorator, ast.Attribute) 
                      and getattr(decorator, 'attr', '') in ['route', 'get', 'post', 'put', 'delete']):
                    api_endpoints.append(func_name)
            
            # استخراج کلاس‌ها
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(item.name)
                
                classes[node.name] = {
                    'methods': methods,
                    'docstring': ast.get_docstring(node) or ''
                }
        
        return imports, functions, classes, api_endpoints
    
    def detect_return_type(self, node):
        """تشخیص نوع داده برگشتی تابع"""
        return_types = []
        
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Return):
                if subnode.value:
                    if isinstance(subnode.value, ast.Dict):
                        return_types.append('dict')
                    elif isinstance(subnode.value, ast.List):
                        return_types.append('list')
                    elif isinstance(subnode.value, ast.Str):
                        return_types.append('str')
                    elif isinstance(subnode.value, ast.Num):
                        return_types.append('int/float')
                    elif isinstance(subnode.value, ast.NameConstant):
                        return_types.append('bool')
                    elif isinstance(subnode.value, ast.Name):
                        return_types.append('variable')
                    else:
                        return_types.append('object')
        
        return list(set(return_types)) if return_types else ['void']
    
    def has_return_statement(self, node):
        """بررسی وجود دستور return در تابع"""
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Return):
                return True
        return False
    
    def analyze_data_flows(self):
        """تحلیل جریان داده بین ماژول‌ها"""
        print("\n📊 در حال تحلیل جریان داده...")
        
        # تحلیل وابستگی‌ها
        for module, info in self.modules_info.items():
            # تحلیل خروجی‌های این ماژول
            outputs = []
            for func_name, func_info in info['functions'].items():
                if func_info['has_return']:
                    return_type = ', '.join(func_info['returns'])
                    outputs.append(f"{func_name}() → {return_type}")
            
            # تحلیل ورودی‌های این ماژول (از طریق پارامترهای توابع)
            inputs = []
            for func_name, func_info in info['functions'].items():
                if func_info['params']:
                    params = ', '.join(func_info['params'])
                    inputs.append(f"{func_name}({params})")
            
            # ذخیره ورودی/خروجی ماژول
            if inputs or outputs:
                self.module_io[module] = {
                    'inputs': inputs[:5],  # فقط ۵ ورودی اول
                    'outputs': outputs[:5],  # فقط ۵ خروجی اول
                    'api_endpoints': info['api_endpoints'],
                    'num_functions': info['num_functions'],
                    'num_classes': info['num_classes']
                }
        
        print(f"  ✅ نقاط ورودی شناسایی شده: {len(self.input_points)}")
        print(f"  ✅ نقاط خروجی شناسایی شده: {len(self.output_points)}")
        print(f"  ✅ ماژول‌های با ورودی/خروجی: {len(self.module_io)}")
    
    def hex_to_rgba(self, hex_color, alpha=1.0):
        """تبدیل رنگ هگز به RGBA (مقادیر 0-1)"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
        elif len(hex_color) == 3:
            r = int(hex_color[0]*2, 16) / 255.0
            g = int(hex_color[1]*2, 16) / 255.0
            b = int(hex_color[2]*2, 16) / 255.0
        else:
            r, g, b = 0.5, 0.5, 0.5
        
        return (r, g, b, alpha)
    
    def generate_flowcharts(self):
        """تولید فلوچارت‌های مختلف"""
        print("\n📊 در حال تولید فلوچارت‌ها...")
        
        # 1. فلوچارت جریان داده کامل
        self.generate_complete_data_flow_chart()
        
        # 2. فلوچارت جریان API
        self.generate_api_flow_chart()
        
        # 3. فلوچارت ورودی-پردازش-خروجی
        self.generate_input_process_output_chart()
        
        # 4. فلوچارت ماژول‌های کلیدی
        self.generate_key_modules_flow_chart()
        
        # 5. فلوچارت جزئیات جریان داده
        self.generate_detailed_data_flow_chart()
        
        print("\n✅ تولید فلوچارت‌ها کامل شد!")
        return True
    
    def generate_complete_data_flow_chart(self):
        """ایجاد فلوچارت کامل جریان داده"""
        print("  🌊 در حال ایجاد فلوچارت جریان داده کامل...")
        
        try:
            fig, ax = plt.subplots(figsize=(24, 16))
            ax.set_xlim(0, 14)
            ax.set_ylim(0, 12)
            
            # عنوان
            ax.text(7, 11.8, '🌊 فلوچارت کامل جریان داده SFS', 
                    ha='center', va='center', fontsize=24, fontweight='bold',
                    path_effects=[path_effects.withStroke(linewidth=3, foreground='white')])
            
            # مراحل اصلی جریان داده
            stages = [
                ('ورودی\nکاربر/API', 1, 9, '#4ECDC4', 'input'),
                ('اعتبارسنجی\n(Validation)', 3.5, 9, '#FF9E6D', 'process'),
                ('پردازش\nمنطق کسب‌وکار', 6, 9, '#FFD166', 'process'),
                ('دسترسی\nداده‌ها', 8.5, 9, '#06D6A0', 'data'),
                ('پردازش\nنهایی', 11, 9, '#118AB2', 'process'),
                ('خروجی\nپاسخ', 13, 9, '#073B4C', 'output')
            ]
            
            # کشیدن مراحل
            for i, (name, x, y, color, stage_type) in enumerate(stages):
                # شکل مرحله
                if stage_type == 'input':
                    shape = patches.Ellipse((x, y), 2.0, 1.2,
                                          facecolor=self.hex_to_rgba(color),
                                          alpha=0.9,
                                          edgecolor='white', linewidth=3)
                elif stage_type == 'output':
                    shape = patches.Ellipse((x, y), 2.0, 1.2,
                                          facecolor=self.hex_to_rgba(color),
                                          alpha=0.9,
                                          edgecolor='white', linewidth=3)
                else:
                    shape = FancyBboxPatch((x-1.0, y-0.6), 2.0, 1.2,
                                          boxstyle=patches.BoxStyle("Round", pad=0.3),
                                          facecolor=self.hex_to_rgba(color),
                                          alpha=0.9,
                                          edgecolor='white', linewidth=3)
                
                ax.add_patch(shape)
                
                # نام مرحله
                ax.text(x, y, name, ha='center', va='center',
                       fontsize=12, fontweight='bold', color='white')
                
                # فلش بین مراحل
                if i < len(stages) - 1:
                    next_x = stages[i+1][1]
                    # خط اصلی
                    ax.annotate('', 
                              xy=(next_x - 1.0, y), 
                              xytext=(x + 1.0, y),
                              arrowprops=dict(arrowstyle='->',
                                            color='#333',
                                            lw=3,
                                            shrinkA=10, shrinkB=10))
            
            # نمایش ماژول‌های واقعی در هر مرحله
            stage_modules = [
                (1, 9, ['API Routes', 'Controllers', 'Webhooks']),
                (3.5, 9, ['Validators', 'Schemas', 'Middleware']),
                (6, 9, ['Services', 'Business Logic', 'Workflows']),
                (8.5, 9, ['Models', 'Repositories', 'Database']),
                (11, 9, ['Serializers', 'Formatters', 'Cache']),
                (13, 9, ['Response', 'JSON/XML', 'Stream'])
            ]
            
            for x, y, module_types in stage_modules:
                for i, mod_type in enumerate(module_types):
                    ax.text(x, y-1.0 - i*0.25, f'• {mod_type}', 
                           ha='center', va='top', fontsize=10)
            
            # جریان داده نمونه
            sample_flow_y = 6
            ax.text(7, sample_flow_y + 1.0, '📋 نمونه جریان داده:', 
                    ha='center', fontsize=16, fontweight='bold')
            
            # جریان از بالا به پایین
            flow_steps = [
                ('1. درخواست API دریافت می‌شود', 7, sample_flow_y),
                ('2. داده‌ها اعتبارسنجی می‌شوند', 7, sample_flow_y - 0.5),
                ('3. منطق کسب‌وکار اجرا می‌شود', 7, sample_flow_y - 1.0),
                ('4. داده از دیتابیس خوانده/نوشته می‌شود', 7, sample_flow_y - 1.5),
                ('5. پاسخ پردازش و فرمت می‌شود', 7, sample_flow_y - 2.0),
                ('6. خروجی به کاربر بازگردانده می‌شود', 7, sample_flow_y - 2.5)
            ]
            
            for text, x, y in flow_steps:
                ax.text(x, y, text, ha='center', va='center',
                       fontsize=11,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='#F8F9FA', edgecolor='gray', alpha=0.8))
                
                # فلش پایین
                if y > sample_flow_y - 2.5:
                    ax.annotate('', xy=(x, y-0.25), xytext=(x, y-0.15),
                              arrowprops=dict(arrowstyle='->', color='green', lw=2))
            
            # آمار جریان داده
            stats_box = FancyBboxPatch((1, 2), 12, 1.5,
                                      boxstyle="round,pad=0.5",
                                      linewidth=2,
                                      edgecolor='#2D3047',
                                      facecolor='#F8F9FA')
            ax.add_patch(stats_box)
            
            total_modules = len(self.modules_info)
            total_flows = sum(len(flows) for flows in self.data_flows.values())
            
            stats_text = f"📊 آمار جریان داده: {total_modules} ماژول | {total_flows} جریان داده"
            ax.text(7, 2.75, stats_text, ha='center', va='center',
                   fontsize=14, fontweight='bold')
            
            ax.axis('off')
            plt.tight_layout()
            output_path = self.project_root / 'complete_data_flow.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"    ✅ ذخیره شد: {output_path}")
        except Exception as e:
            print(f"    ❌ خطا در ایجاد فلوچارت کامل: {e}")
    
    def generate_api_flow_chart(self):
        """ایجاد فلوچارت جریان API"""
        print("  🔄 در حال ایجاد فلوچارت جریان API...")
        
        try:
            fig, ax = plt.subplots(figsize=(22, 14))
            ax.set_xlim(0, 12)
            ax.set_ylim(0, 10)
            
            ax.text(6, 9.8, '🌐 فلوچارت جریان API در SFS', 
                    ha='center', va='center', fontsize=22, fontweight='bold')
            
            # ساختار جریان API
            api_flow = [
                ('کلاینت\n(مرورگر/اپ)', 1, 8, '#4ECDC4'),
                ('API Gateway\n/Load Balancer', 3, 8, '#FF9E6D'),
                ('سرور وب\n(FastAPI/Django)', 5, 8, '#FFD166'),
                ('مسیریابی\n(Routing)', 7, 8, '#06D6A0'),
                ('کنترلرها\n(Controllers)', 9, 8, '#118AB2'),
                ('سرویس‌ها\n(Services)', 11, 8, '#073B4C')
            ]
            
            # کشیدن جریان API
            for i, (name, x, y, color) in enumerate(api_flow):
                # شکل با گوشه‌های گرد
                shape = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1.0,
                                      boxstyle=patches.BoxStyle("Round", pad=0.2),
                                      facecolor=self.hex_to_rgba(color),
                                      edgecolor='white',
                                      linewidth=2)
                ax.add_patch(shape)
                
                # نام
                ax.text(x, y, name, ha='center', va='center',
                       fontsize=10, fontweight='bold', color='white')
                
                # فلش به جلو
                if i < len(api_flow) - 1:
                    next_x = api_flow[i+1][1]
                    ax.annotate('', 
                              xy=(next_x - 0.8, y), 
                              xytext=(x + 0.8, y),
                              arrowprops=dict(arrowstyle='->',
                                            color='blue',
                                            lw=2))
            
            # جریان بازگشت پاسخ
            return_flow_y = 6
            ax.text(6, return_flow_y + 0.8, '🔙 جریان بازگشت پاسخ:', 
                    ha='center', fontsize=14, fontweight='bold')
            
            return_steps = [
                ('سرویس‌ها', 11, return_flow_y),
                ('کنترلرها', 9, return_flow_y),
                ('مسیریابی', 7, return_flow_y),
                ('سرور وب', 5, return_flow_y),
                ('API Gateway', 3, return_flow_y),
                ('کلاینت', 1, return_flow_y)
            ]
            
            for i, (name, x, y) in enumerate(return_steps):
                color = '#96CEB4' if i % 2 == 0 else '#FFEAA7'
                shape = FancyBboxPatch((x-0.7, y-0.4), 1.4, 0.8,
                                      boxstyle=patches.BoxStyle("Round", pad=0.1),
                                      facecolor=self.hex_to_rgba(color),
                                      edgecolor='white',
                                      linewidth=1.5)
                ax.add_patch(shape)
                
                ax.text(x, y, name, ha='center', va='center',
                       fontsize=9, fontweight='bold', color='#333')
                
                # فلش به عقب
                if i < len(return_steps) - 1:
                    next_x = return_steps[i+1][1]
                    ax.annotate('', 
                              xy=(next_x + 0.7, y), 
                              xytext=(x - 0.7, y),
                              arrowprops=dict(arrowstyle='->',
                                            color='red',
                                            lw=2,
                                            connectionstyle="arc3,rad=-0.2"))
            
            # نمایش نمونه API endpoints واقعی
            endpoints_y = 4
            ax.text(6, endpoints_y + 0.5, '🎯 نمونه Endpoint‌های واقعی:', 
                    ha='center', fontsize=14, fontweight='bold')
            
            # جمع‌آوری endpointهای واقعی
            real_endpoints = []
            for module, info in self.modules_info.items():
                if info['api_endpoints']:
                    for endpoint in info['api_endpoints'][:2]:  # فقط ۲ endpoint اول هر ماژول
                        real_endpoints.append(f"{module.split('.')[-1]}.{endpoint}")
            
            # نمایش endpointها
            cols = 3
            for i, endpoint in enumerate(real_endpoints[:9]):  # حداکثر ۹ endpoint
                col = i % cols
                row = i // cols
                
                x = 2 + col * 3
                y = endpoints_y - row * 0.4
                
                ax.text(x, y, f'• {endpoint[:20]}', 
                       ha='left', fontsize=9,
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='lightyellow', alpha=0.7))
            
            ax.axis('off')
            plt.tight_layout()
            output_path = self.project_root / 'api_flow_chart.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"    ✅ ذخیره شد: {output_path}")
        except Exception as e:
            print(f"    ❌ خطا در ایجاد فلوچارت API: {e}")
    
    def generate_input_process_output_chart(self):
        """ایجاد فلوچارت ورودی-پردازش-خروجی"""
        print("  🔄 در حال ایجاد فلوچارت ورودی-پردازش-خروجی...")
        
        try:
            # انتخاب ماژول‌های کلیدی برای نمایش
            key_modules = []
            for module, io_info in self.module_io.items():
                if io_info.get('inputs') and io_info.get('outputs'):
                    key_modules.append((module, io_info))
            
            if not key_modules:
                print("  ⚠️ ماژول با ورودی/خروجی یافت نشد")
                return
            
            # انتخاب ۶ ماژول برتر
            key_modules = key_modules[:6]
            
            fig, axes = plt.subplots(2, 3, figsize=(20, 12))
            axes = axes.flatten()
            
            fig.suptitle('📊 فلوچارت ورودی-پردازش-خروجی ماژول‌های کلیدی', 
                        fontsize=22, fontweight='bold', y=0.98)
            
            for idx, (module_name, io_info) in enumerate(key_modules):
                ax = axes[idx]
                ax.set_xlim(0, 10)
                ax.set_ylim(0, 10)
                
                # تعیین رنگ بر اساس نوع ماژول
                if 'backend' in module_name.lower():
                    color = '#FF6B6B'
                    mtype = 'Backend'
                elif 'frontend' in module_name.lower():
                    color = '#4ECDC4'
                    mtype = 'Frontend'
                else:
                    color = '#96CEB4'
                    mtype = 'General'
                
                # عنوان ماژول
                short_name = module_name.split('.')[-1][:15]
                ax.text(5, 9.5, f'📦 {short_name} ({mtype})', 
                       ha='center', va='center', fontsize=14, fontweight='bold', color=color)
                
                # بخش ورودی‌ها (سمت چپ)
                ax.text(2.5, 8.5, '📥 ورودی‌ها:', fontsize=12, fontweight='bold', ha='center')
                
                inputs = io_info.get('inputs', [])
                for i, inp in enumerate(inputs[:3]):  # فقط ۳ ورودی اول
                    ax.text(2.5, 8.0 - i*0.35, f'→ {inp[:15]}', 
                           ha='center', fontsize=9)
                
                # بخش پردازش (مرکز)
                process_shape = FancyBboxPatch((4, 6), 2, 1.5,
                                              boxstyle=patches.BoxStyle("Round", pad=0.3),
                                              facecolor=self.hex_to_rgba(color),
                                              edgecolor=color,
                                              linewidth=3)
                ax.add_patch(process_shape)
                ax.text(5, 6.75, 'پردازش', 
                       ha='center', va='center',
                       fontsize=12, fontweight='bold', color='white')
                
                # آمار پردازش
                stats_text = f"{io_info.get('num_functions', 0)} توابع\n{io_info.get('num_classes', 0)} کلاس‌ها"
                ax.text(5, 6.0, stats_text, ha='center', va='center',
                       fontsize=10, color='white')
                
                # بخش خروجی‌ها (سمت راست)
                ax.text(7.5, 8.5, '📤 خروجی‌ها:', fontsize=12, fontweight='bold', ha='center')
                
                outputs = io_info.get('outputs', [])
                for i, out in enumerate(outputs[:3]):  # فقط ۳ خروجی اول
                    ax.text(7.5, 8.0 - i*0.35, f'← {out[:15]}', 
                           ha='center', fontsize=9)
                
                # فلش‌های جریان داده
                # ورودی به پردازش
                ax.annotate('', xy=(4, 6.75), xytext=(3, 7.0),
                          arrowprops=dict(arrowstyle='->', color='blue', lw=2, alpha=0.7))
                
                # پردازش به خروجی
                ax.annotate('', xy=(6, 6.75), xytext=(7, 7.0),
                          arrowprops=dict(arrowstyle='->', color='green', lw=2, alpha=0.7))
                
                ax.axis('off')
            
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            output_path = self.project_root / 'input_process_output.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"    ✅ ذخیره شد: {output_path}")
        except Exception as e:
            print(f"    ❌ خطا در ایجاد فلوچارت IPO: {e}")
    
    def generate_key_modules_flow_chart(self):
        """ایجاد فلوچارت جریان بین ماژول‌های کلیدی"""
        print("  🔗 در حال ایجاد فلوچارت جریان بین ماژول‌های کلیدی...")
        
        try:
            # پیدا کردن ماژول‌های با بیشترین ارتباط
            module_connections = []
            for module in self.graph.nodes():
                indegree = self.graph.in_degree(module)
                outdegree = self.graph.out_degree(module)
                total_connections = indegree + outdegree
                if total_connections > 0:
                    module_connections.append((module, total_connections, indegree, outdegree))
            
            if not module_connections:
                print("  ⚠️ ارتباطی بین ماژول‌ها یافت نشد")
                return
            
            # مرتب‌سازی و انتخاب ۸ ماژول برتر
            module_connections.sort(key=lambda x: x[1], reverse=True)
            key_modules = module_connections[:8]
            
            fig, ax = plt.subplots(figsize=(20, 14))
            ax.set_xlim(0, 14)
            ax.set_ylim(0, 12)
            
            ax.text(7, 11.8, '🔗 فلوچارت جریان داده بین ماژول‌های کلیدی', 
                    ha='center', va='center', fontsize=22, fontweight='bold')
            
            # موقعیت‌دهی ماژول‌ها در دایره
            radius = 4.0
            center_x, center_y = 7, 6
            
            for i, (module, total_conn, indegree, outdegree) in enumerate(key_modules):
                angle = 2 * np.pi * i / len(key_modules)
                x = center_x + radius * np.cos(angle)
                y = center_y + radius * np.sin(angle)
                
                # رنگ بر اساس نوع
                module_lower = module.lower()
                if 'backend' in module_lower:
                    color = '#FF6B6B'
                elif 'frontend' in module_lower:
                    color = '#4ECDC4'
                else:
                    color = '#96CEB4'
                
                # کشیدن ماژول
                circle = Circle((x, y), 0.8,
                              facecolor=self.hex_to_rgba(color, 0.8),
                              edgecolor='white',
                              linewidth=3)
                ax.add_patch(circle)
                
                # نام ماژول
                short_name = module.split('.')[-1][:10]
                ax.text(x, y, short_name, 
                       ha='center', va='center',
                       fontsize=10, fontweight='bold',
                       color='white',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
                
                # اطلاعات ارتباطات
                conn_text = f"←{indegree} →{outdegree}"
                ax.text(x, y-1.0, conn_text, 
                       ha='center', va='center',
                       fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.7))
                
                # نمایش ورودی/خروجی
                io_info = self.module_io.get(module, {})
                if io_info:
                    # ورودی‌ها
                    if io_info.get('inputs'):
                        input_text = io_info['inputs'][0][:15] if len(io_info['inputs'][0]) > 15 else io_info['inputs'][0]
                        ax.text(x-1.5, y+0.5, f"📥 {input_text}", 
                               ha='right', va='center', fontsize=8,
                               bbox=dict(boxstyle="round,pad=0.1", facecolor='lightblue', alpha=0.6))
                    
                    # خروجی‌ها
                    if io_info.get('outputs'):
                        output_text = io_info['outputs'][0][:15] if len(io_info['outputs'][0]) > 15 else io_info['outputs'][0]
                        ax.text(x+1.5, y+0.5, f"📤 {output_text}", 
                               ha='left', va='center', fontsize=8,
                               bbox=dict(boxstyle="round,pad=0.1", facecolor='lightgreen', alpha=0.6))
            
            # کشیدن ارتباطات بین ماژول‌ها
            for i, (module1, _, _, _) in enumerate(key_modules):
                for j, (module2, _, _, _) in enumerate(key_modules):
                    if i < j:  # فقط یک بار بین هر جفت
                        # بررسی وجود ارتباط در گراف
                        if self.graph.has_edge(module1, module2):
                            # موقعیت ماژول‌ها
                            angle1 = 2 * np.pi * i / len(key_modules)
                            angle2 = 2 * np.pi * j / len(key_modules)
                            
                            x1 = center_x + radius * np.cos(angle1)
                            y1 = center_y + radius * np.sin(angle1)
                            x2 = center_x + radius * np.cos(angle2)
                            y2 = center_y + radius * np.sin(angle2)
                            
                            # کشیدن خط ارتباط
                            ax.annotate('', 
                                      xy=(x2, y2), 
                                      xytext=(x1, y1),
                                      arrowprops=dict(arrowstyle='->',
                                                    color='gray',
                                                    alpha=0.5,
                                                    lw=1.5,
                                                    connectionstyle="arc3,rad=0.2"))
            
            # ماژول مرکزی (با بیشترین ارتباط)
            if key_modules:
                central_module = key_modules[0][0]
                central_circle = Circle((center_x, center_y), 1.0,
                                      facecolor=self.hex_to_rgba('gold', 0.9),
                                      edgecolor='darkorange',
                                      linewidth=4)
                ax.add_patch(central_circle)
                
                ax.text(center_x, center_y, 'مرکزی', 
                       ha='center', va='center',
                       fontsize=12, fontweight='bold',
                       color='darkorange')
                
                conn_info = f"{key_modules[0][1]} ارتباط"
                ax.text(center_x, center_y - 1.3, conn_info, 
                       ha='center', va='center',
                       fontsize=10, fontweight='bold')
            
            ax.axis('off')
            plt.tight_layout()
            output_path = self.project_root / 'key_modules_flow.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"    ✅ ذخیره شد: {output_path}")
        except Exception as e:
            print(f"    ❌ خطا در ایجاد فلوچارت ماژول‌های کلیدی: {e}")
    
    def generate_detailed_data_flow_chart(self):
        """ایجاد فلوچارت جزئیات جریان داده"""
        print("  🔍 در حال ایجاد فلوچارت جزئیات جریان داده...")
        
        try:
            # انتخاب ماژول‌های ورودی و خروجی واقعی
            input_modules = []
            output_modules = []
            
            for module, info in self.modules_info.items():
                if info['api_endpoints']:
                    input_modules.append(module)
                if any('get_' in func.lower() or 'create_' in func.lower() 
                      for func in info['functions'].keys()):
                    output_modules.append(module)
            
            # انتخاب نمونه‌ها
            input_samples = input_modules[:3]
            output_samples = output_modules[:3]
            
            if not input_samples and not output_samples:
                print("  ⚠️ ماژول ورودی/خروجی یافت نشد")
                return
            
            fig, ax = plt.subplots(figsize=(22, 12))
            ax.set_xlim(0, 14)
            ax.set_ylim(0, 10)
            
            ax.text(7, 9.8, '🔬 فلوچارت جزئیات جریان داده SFS', 
                    ha='center', va='center', fontsize=22, fontweight='bold')
            
            # بخش ورودی‌ها
            input_x = 2
            ax.text(input_x, 8.5, '🎯 نقاط ورودی سیستم:', 
                    ha='center', fontsize=16, fontweight='bold', color='#4ECDC4')
            
            for i, module in enumerate(input_samples[:5]):  # حداکثر ۵ ورودی
                short_name = module.split('.')[-1]
                y_pos = 7.5 - i * 1.2
                
                # کادر ورودی
                input_box = FancyBboxPatch((input_x-1.5, y_pos-0.5), 3, 1.0,
                                          boxstyle=patches.BoxStyle("Round", pad=0.3),
                                          facecolor=self.hex_to_rgba('#4ECDC4', 0.8),
                                          edgecolor='white',
                                          linewidth=2)
                ax.add_patch(input_box)
                
                ax.text(input_x, y_pos, short_name, 
                       ha='center', va='center',
                       fontsize=11, fontweight='bold', color='white')
                
                # نمایش endpointها
                module_info = self.modules_info.get(module, {})
                if module_info.get('api_endpoints'):
                    endpoints = module_info['api_endpoints'][:2]
                    for j, endpoint in enumerate(endpoints):
                        ax.text(input_x, y_pos-0.3 - j*0.2, f'• {endpoint}', 
                               ha='center', fontsize=9, color='white')
                
                # فلش خروجی از ورودی
                ax.annotate('', 
                          xy=(input_x+2.0, y_pos), 
                          xytext=(input_x+1.5, y_pos),
                          arrowprops=dict(arrowstyle='->',
                                        color='blue',
                                        lw=2))
            
            # بخش پردازش مرکزی
            process_x = 7
            process_y = 4.5
            process_width = 4
            process_height = 5
            
            # کادر پردازش
            process_box = FancyBboxPatch((process_x-2, process_y-2.5), process_width, process_height,
                                        boxstyle=patches.BoxStyle("Round", pad=0.5),
                                        facecolor=self.hex_to_rgba('#FFD166', 0.3),
                                        edgecolor='#FFD166',
                                        linewidth=3)
            ax.add_patch(process_box)
            
            ax.text(process_x, process_y+2.0, '⚙️ مرکز پردازش داده', 
                   ha='center', va='center',
                   fontsize=18, fontweight='bold', color='#FFD166')
            
            # ماژول‌های پردازش داخلی
            internal_modules = []
            for module, io_info in self.module_io.items():
                if io_info.get('inputs') and io_info.get('outputs'):
                    if module not in input_samples and module not in output_samples:
                        internal_modules.append(module)
            
            # نمایش ماژول‌های پردازش داخلی
            cols = 2
            for i, module in enumerate(internal_modules[:8]):  # حداکثر ۸ ماژول
                col = i % cols
                row = i // cols
                
                x = process_x - 1.5 + col * 3
                y = process_y + 1.0 - row * 1.2
                
                short_name = module.split('.')[-1][:12]
                
                # کادر ماژول داخلی
                mod_box = FancyBboxPatch((x-1.0, y-0.4), 2.0, 0.8,
                                        boxstyle=patches.BoxStyle("Round", pad=0.2),
                                        facecolor=self.hex_to_rgba('#06D6A0', 0.7),
                                        edgecolor='white',
                                        linewidth=1.5)
                ax.add_patch(mod_box)
                
                ax.text(x, y, short_name, 
                       ha='center', va='center',
                       fontsize=9, fontweight='bold', color='white')
                
                # اطلاعات IO
                io_info = self.module_io.get(module, {})
                if io_info.get('inputs') and io_info.get('outputs'):
                    ax.text(x, y-0.3, f"📥{len(io_info['inputs'])} 📤{len(io_info['outputs'])}", 
                           ha='center', fontsize=8, color='white')
            
            # بخش خروجی‌ها
            output_x = 12
            ax.text(output_x, 8.5, '📊 نقاط خروجی سیستم:', 
                    ha='center', fontsize=16, fontweight='bold', color='#073B4C')
            
            for i, module in enumerate(output_samples[:5]):  # حداکثر ۵ خروجی
                short_name = module.split('.')[-1]
                y_pos = 7.5 - i * 1.2
                
                # کادر خروجی
                output_box = FancyBboxPatch((output_x-1.5, y_pos-0.5), 3, 1.0,
                                           boxstyle=patches.BoxStyle("Round", pad=0.3),
                                           facecolor=self.hex_to_rgba('#073B4C', 0.8),
                                           edgecolor='white',
                                           linewidth=2)
                ax.add_patch(output_box)
                
                ax.text(output_x, y_pos, short_name, 
                       ha='center', va='center',
                       fontsize=11, fontweight='bold', color='white')
                
                # نمایش توابع خروجی
                module_info = self.modules_info.get(module, {})
                if module_info.get('functions'):
                    # پیدا کردن توابع خروجی
                    output_funcs = [f for f in module_info['functions'].keys() 
                                  if any(keyword in f.lower() 
                                        for keyword in ['get_', 'create_', 'save_', 'return_'])]
                    
                    for j, func in enumerate(output_funcs[:2]):
                        ax.text(output_x, y_pos-0.3 - j*0.2, f'• {func}()', 
                               ha='center', fontsize=9, color='white')
                
                # فلش ورودی به خروجی
                ax.annotate('', 
                          xy=(output_x-1.5, y_pos), 
                          xytext=(output_x-2.0, y_pos),
                          arrowprops=dict(arrowstyle='->',
                                        color='green',
                                        lw=2))
            
            # فلش‌های جریان داده کلی
            # از ورودی به پردازش
            ax.annotate('', 
                      xy=(process_x-2, 5), 
                      xytext=(input_x+2, 5),
                      arrowprops=dict(arrowstyle='->',
                                    color='blue',
                                    lw=3,
                                    connectionstyle="arc3,rad=0.2"))
            
            ax.text((input_x+process_x)/2, 5.5, 'جریان داده ورودی', 
                   ha='center', fontsize=11, fontweight='bold', color='blue')
            
            # از پردازش به خروجی
            ax.annotate('', 
                      xy=(output_x-2, 3), 
                      xytext=(process_x+2, 3),
                      arrowprops=dict(arrowstyle='->',
                                    color='green',
                                    lw=3,
                                    connectionstyle="arc3,rad=0.2"))
            
            ax.text((process_x+output_x)/2, 3.5, 'جریان داده خروجی', 
                   ha='center', fontsize=11, fontweight='bold', color='green')
            
            ax.axis('off')
            plt.tight_layout()
            output_path = self.project_root / 'detailed_data_flow.png'
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"    ✅ ذخیره شد: {output_path}")
            
            # همچنین یک گزارش متنی از جریان داده ایجاد می‌کنیم
            self.generate_data_flow_report()
            
        except Exception as e:
            print(f"    ❌ خطا در ایجاد فلوچارت جزئیات: {e}")
    
    def generate_data_flow_report(self):
        """ایجاد گزارش متنی از جریان داده"""
        report_path = self.project_root / 'data_flow_report.txt'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("گزارش تحلیل جریان داده سیستم SFS\n")
            f.write("="*80 + "\n\n")
            
            f.write("📊 آمار کلی:\n")
            f.write(f"  • تعداد ماژول‌ها: {len(self.modules_info)}\n")
            f.write(f"  • نقاط ورودی شناسایی شده: {len(self.input_points)}\n")
            f.write(f"  • نقاط خروجی شناسایی شده: {len(self.output_points)}\n")
            f.write(f"  • ماژول‌های با ورودی/خروجی مشخص: {len(self.module_io)}\n\n")
            
            f.write("🎯 نقاط ورودی اصلی:\n")
            for i, (module, endpoint) in enumerate(self.input_points[:10], 1):
                f.write(f"  {i}. {module}.{endpoint}\n")
            
            f.write("\n📊 نقاط خروجی اصلی:\n")
            for i, (module, func) in enumerate(self.output_points[:10], 1):
                f.write(f"  {i}. {module}.{func}\n")
            
            f.write("\n🔗 ماژول‌های کلیدی با بیشترین ارتباط:\n")
            # محاسبه ارتباطات
            module_connections = []
            for module in self.graph.nodes():
                indegree = self.graph.in_degree(module)
                outdegree = self.graph.out_degree(module)
                total = indegree + outdegree
                if total > 0:
                    module_connections.append((module, total, indegree, outdegree))
            
            module_connections.sort(key=lambda x: x[1], reverse=True)
            
            for i, (module, total, indegree, outdegree) in enumerate(module_connections[:15], 1):
                f.write(f"  {i}. {module} (کل: {total}, ورودی: {indegree}, خروجی: {outdegree})\n")
            
            f.write("\n💡 توصیه‌های بهبود جریان داده:\n")
            recommendations = [
                "1. ماژول‌های با وابستگی زیاد را modularize کنید",
                "2. نقاط ورودی/خروجی را با validation قوی محافظت کنید",
                "3. از الگوی Repository برای دسترسی به داده‌ها استفاده کنید",
                "4. لاگ‌گیری جامع در نقاط کلیدی جریان داده",
                "5. تست end-to-end برای جریان‌های داده اصلی"
            ]
            
            for rec in recommendations:
                f.write(f"  • {rec}\n")
        
        print(f"    📄 گزارش متنی: {report_path}")

def main():
    """تابع اصلی"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='تحلیل دقیق جریان داده در سیستم SFS')
    parser.add_argument('--path', default='.', help='مسیر پروژه')
    parser.add_argument('--dirs', nargs='+', default=['sfs/backend', 'sfs/frontend'],
                       help='مسیرهای مشخص شده برای اسکن')
    
    args = parser.parse_args()
    
    project_path = Path(args.path).resolve()
    
    if not project_path.exists():
        print(f"❌ مسیر وجود ندارد: {project_path}")
        return
    
    print("="*60)
    print("🔬 تحلیلگر جریان داده SFS")
    print("="*60)
    print(f"📁 مسیر پروژه: {project_path}")
    print(f"📂 مسیرهای اسکن: {args.dirs}")
    
    # ایجاد analyzer
    analyzer = DataFlowAnalyzer(project_path, args.dirs)
    
    # اجرای تحلیل
    result = analyzer.scan_project()
    
    if result is None:
        print("\n⚠️ هیچ فایل معتبری برای تحلیل یافت نشد!")
        return
    
    print("\n" + "="*60)
    print("✅ تحلیل جریان داده کامل شد!")
    print("="*60)
    print("\n📊 فلوچارت‌های تولید شده:")
    print("  1. complete_data_flow.png     - فلوچارت کامل جریان داده")
    print("  2. api_flow_chart.png        - فلوچارت جریان API")
    print("  3. input_process_output.png  - فلوچارت ورودی-پردازش-خروجی")
    print("  4. key_modules_flow.png      - فلوچارت ماژول‌های کلیدی")
    print("  5. detailed_data_flow.png    - فلوچارت جزئیات جریان داده")
    print("  6. data_flow_report.txt      - گزارش متنی تحلیل جریان داده")
    print("\n🚀 برای مشاهده، فایل‌های PNG را باز کنید.")

if __name__ == "__main__":
    # نصب پکیج‌های مورد نیاز
    import subprocess
    import sys
    
    required_packages = ['networkx', 'matplotlib', 'numpy']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"📦 در حال نصب {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    # غیرفعال کردن هشدارها
    warnings.filterwarnings('ignore')
    
    main()