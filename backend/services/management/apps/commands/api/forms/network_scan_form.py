from django import forms


class NetworkScanForm(forms.Form):
    edge_node_id = forms.CharField(max_length=64, label="Edge node")
