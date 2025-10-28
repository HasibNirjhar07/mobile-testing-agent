"""
Report Generator - Creates HTML/PDF test reports
"""
import json
from pathlib import Path
from datetime import datetime
from loguru import logger

class ReportGenerator:
    def __init__(self, config):
        self.config = config
        self.output_dir = Path(config['report']['output_dir'])
        self.output_dir.mkdir(exist_ok=True)
    
    def generate(self, test_summary, apk_info):
        """Generate test report"""
        logger.info("Generating test report...")
        
        report_format = self.config['report']['format']
        
        if report_format == 'html':
            return self._generate_html(test_summary, apk_info)
        elif report_format == 'json':
            return self._generate_json(test_summary, apk_info)
        elif report_format == 'pdf':
            return self._generate_pdf(test_summary, apk_info)
        else:
            logger.error(f"Unknown report format: {report_format}")
            return None
    
    def _generate_html(self, test_summary, apk_info):
        """Generate HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.html"
        filepath = self.output_dir / filename
        
        html_content = self._create_html_content(test_summary, apk_info)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {filepath}")
        return str(filepath)
    
    def _generate_json(self, test_summary, apk_info):
        """Generate JSON report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.json"
        filepath = self.output_dir / filename
        
        report_data = {
            'apk_info': apk_info,
            'test_summary': test_summary,
            'timestamp': timestamp
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"JSON report generated: {filepath}")
        return str(filepath)
    
    def _create_html_content(self, test_summary, apk_info):
        """Create HTML report content"""
        total = test_summary['total_tests']
        passed = test_summary['passed']
        failed = test_summary['failed']
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile App Test Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .total {{ color: #007bff; }}
        .screens {{ color: #17a2b8; }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .app-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        
        .app-info-item {{
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .app-info-item:last-child {{
            border-bottom: none;
        }}
        
        .app-info-label {{
            font-weight: bold;
            width: 200px;
            color: #555;
        }}
        
        .app-info-value {{
            flex: 1;
            color: #333;
        }}
        
        .test-results {{
            display: grid;
            gap: 20px;
        }}
        
        .test-item {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s;
        }}
        
        .test-item:hover {{
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .test-name {{
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
        }}
        
        .test-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .status-pass {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .test-details {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.9em;
        }}
        
        .screenshot {{
            margin-top: 15px;
        }}
        
        .screenshot img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: pointer;
            transition: transform 0.3s;
        }}
        
        .screenshot img:hover {{
            transform: scale(1.02);
        }}
        
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 1s;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
        }}
        
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 Mobile App Test Report</h1>
            <p>Automated Testing Results - {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-label">Total Tests</div>
                <div class="stat-number total">{total}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Passed</div>
                <div class="stat-number passed">{passed}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Failed</div>
                <div class="stat-number failed">{failed}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Screens Explored</div>
                <div class="stat-number screens">{test_summary['screens_explored']}</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Test Summary</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pass_rate}%">
                        {pass_rate:.1f}% Pass Rate
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>📦 Application Information</h2>
                <div class="app-info">
                    <div class="app-info-item">
                        <div class="app-info-label">Package Name:</div>
                        <div class="app-info-value">{apk_info.get('package_name', 'N/A')}</div>
                    </div>
                    <div class="app-info-item">
                        <div class="app-info-label">Main Activity:</div>
                        <div class="app-info-value">{apk_info.get('main_activity', 'N/A')}</div>
                    </div>
                    <div class="app-info-item">
                        <div class="app-info-label">Total Screens:</div>
                        <div class="app-info-value">{test_summary['screens_explored']}</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🧪 Test Results</h2>
                <div class="test-results">
"""
        
        # Add test results
        for result in test_summary['test_results']:
            status_class = 'status-pass' if result['status'] == 'PASS' else 'status-fail'
            details_html = ""
            
            if result.get('details'):
                details = result['details']
                details_html = f"""
                <div class="test-details">
                    <strong>Element Type:</strong> {details.get('type', 'N/A')}<br>
                    <strong>Text:</strong> {details.get('text', 'N/A')}<br>
                    <strong>Resource ID:</strong> {details.get('resource_id', 'N/A')}<br>
                    <strong>Content Description:</strong> {details.get('content_desc', 'N/A')}
                </div>
"""
            
            screenshot_html = ""
            if result.get('screenshot'):
                screenshot_html = f"""
                <div class="screenshot">
                    <img src="../{result['screenshot']}" alt="Screenshot" loading="lazy">
                </div>
"""
            
            html += f"""
                    <div class="test-item">
                        <div class="test-header">
                            <div class="test-name">{result['test_name']}</div>
                            <div class="test-status {status_class}">{result['status']}</div>
                        </div>
                        {details_html}
                        {screenshot_html}
                    </div>
"""
        
        html += """
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Automated Mobile App Testing Agent</p>
            <p>Powered by Python + Appium + AI</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def _generate_pdf(self, test_summary, apk_info):
        """Generate PDF report (requires HTML first)"""
        try:
            from weasyprint import HTML
            
            # First generate HTML
            html_content = self._create_html_content(test_summary, apk_info)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_report_{timestamp}.pdf"
            filepath = self.output_dir / filename
            
            # Convert to PDF
            HTML(string=html_content).write_pdf(filepath)
            
            logger.info(f"PDF report generated: {filepath}")
            return str(filepath)
            
        except ImportError:
            logger.error("WeasyPrint not installed. Install with: pip install weasyprint")
            return None
        except Exception as e:
            logger.error(f"Failed to generate PDF: {str(e)}")
            return None