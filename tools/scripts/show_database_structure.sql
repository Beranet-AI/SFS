-- ============================================
-- SFS DATABASE STRUCTURE ANALYZER - ENGLISH
-- Clean version without encoding issues
-- ============================================

-- Section 1: Database Info
SELECT '=== DATABASE INFORMATION ===' as section;
SELECT 
    'Database: ' || current_database() as info,
    'User: ' || current_user as info,
    'PostgreSQL Version: ' || version() as info,
    'Time: ' || now() as info;

-- Section 2: All Tables
SELECT E'\n=== ALL TABLES (26 tables) ===' as section;
SELECT 
    tablename as table_name,
    (SELECT COUNT(*) FROM information_schema.columns c 
     WHERE c.table_name = t.tablename AND c.table_schema = t.schemaname) as columns_count,
    (SELECT c.reltuples::bigint FROM pg_class c 
     WHERE c.relname = t.tablename) as estimated_rows
FROM pg_tables t
WHERE t.schemaname = 'public'
ORDER BY t.tablename;

-- Section 3: Table Sizes
SELECT E'\n=== TABLE SIZES ===' as section;
SELECT 
    tablename as table_name,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as total_size,
    pg_size_pretty(pg_relation_size(tablename::regclass)) as table_size,
    pg_size_pretty(pg_indexes_size(tablename::regclass)) as indexes_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;

-- Section 4: Domain Analysis
SELECT E'\n=== DOMAIN ANALYSIS ===' as section;
WITH domain_groups AS (
    SELECT 
        tablename,
        CASE 
            WHEN tablename LIKE '%command%' THEN 'COMMANDS'
            WHEN tablename LIKE '%farm%' THEN 'FARMS'
            WHEN tablename LIKE '%livestock%' THEN 'LIVESTOCK'
            WHEN tablename LIKE '%device%' THEN 'DEVICES'
            WHEN tablename LIKE '%health%' THEN 'HEALTH'
            WHEN tablename LIKE '%incident%' THEN 'INCIDENTS'
            WHEN tablename LIKE '%user%' OR tablename LIKE '%auth%' THEN 'AUTHENTICATION'
            WHEN tablename LIKE '%django%' THEN 'DJANGO SYSTEM'
            ELSE 'OTHER'
        END as domain
    FROM pg_tables
    WHERE schemaname = 'public'
)
SELECT 
    domain,
    COUNT(*) as table_count,
    STRING_AGG(tablename, ', ' ORDER BY tablename) as tables
FROM domain_groups
GROUP BY domain
ORDER BY table_count DESC;

-- Section 5: Key Relationships
SELECT E'\n=== KEY RELATIONSHIPS ===' as section;
SELECT
    tc.table_name as from_table,
    ccu.table_name as to_table,
    kcu.column_name as via_column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu 
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu 
    ON tc.constraint_name = ccu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
    AND tc.table_name NOT LIKE '%django%'
    AND tc.table_name NOT LIKE '%auth%'
ORDER BY tc.table_name;

-- Section 6: Summary
SELECT E'\n=== DATABASE SUMMARY ===' as section;
WITH stats AS (
    SELECT 
        COUNT(DISTINCT t.tablename) as total_tables,
        COUNT(DISTINCT c.column_name) as total_columns,
        COUNT(DISTINCT tc.constraint_name) FILTER (WHERE tc.constraint_type = 'FOREIGN KEY') as foreign_keys,
        COUNT(DISTINCT idx.indexname) as total_indexes,
        pg_size_pretty(pg_database_size('sfs')) as db_size
    FROM pg_tables t
    LEFT JOIN information_schema.columns c 
        ON t.tablename = c.table_name AND t.schemaname = c.table_schema
    LEFT JOIN information_schema.table_constraints tc 
        ON t.tablename = tc.table_name AND t.schemaname = tc.table_schema
    LEFT JOIN pg_indexes idx 
        ON t.tablename = idx.tablename AND t.schemaname = idx.schemaname
    WHERE t.schemaname = 'public'
)
SELECT 
    'Total Tables' as metric, 
    total_tables::text as value
FROM stats
UNION ALL
SELECT 'Total Columns', total_columns::text
FROM stats
UNION ALL
SELECT 'Foreign Keys', foreign_keys::text
FROM stats
UNION ALL
SELECT 'Indexes', total_indexes::text
FROM stats
UNION ALL
SELECT 'Database Size', db_size
FROM stats;

-- Section 7: Recommendations
SELECT E'\n=== RECOMMENDATIONS ===' as section;
SELECT 
    '1. Large tables to monitor:' as recommendation,
    tablename as table_name,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size
FROM pg_tables
WHERE schemaname = 'public' 
    AND pg_total_relation_size(tablename::regclass) > 100000
ORDER BY pg_total_relation_size(tablename::regclass) DESC
LIMIT 5;