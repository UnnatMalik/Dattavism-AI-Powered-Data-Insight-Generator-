from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import markdown
import re
import matplotlib.pyplot as plt
import seaborn as sns
import io
import datetime

class EnhancedReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_styles()
        
    def setup_styles(self):
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1A237E'),
            leading=28
        )
        
        # Section heading style
        self.section_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=16,
            spaceAfter=12,
            textColor=colors.HexColor('#303F9F'),
            leading=20,
            borderColor=colors.HexColor('#303F9F'),
            borderWidth=1,
            borderPadding=5
        )
        
        # Subsection style
        self.subsection_style = ParagraphStyle(
            'SubsectionHeading',
            parent=self.styles['Heading3'],
            fontSize=13,
            spaceBefore=12,
            spaceAfter=8,
            textColor=colors.HexColor('#3949AB'),
            leading=16
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'BodyStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
            textColor=colors.HexColor('#333333')
        )
        
        # Caption style for charts
        self.caption_style = ParagraphStyle(
            'CaptionStyle',
            parent=self.styles['Italic'],
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666'),
            spaceBefore=4,
            spaceAfter=12
        )

    def create_cover_page(self, title):
        elements = []
        
        # Add header with line
        elements.append(Paragraph("Data Analysis Report", self.caption_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Title with background
        title_with_style = ParagraphStyle(
            'TitleWithBackground',
            parent=self.title_style,
            backColor=colors.HexColor('#F5F5F5'),
            borderColor=colors.HexColor('#1A237E'),
            borderWidth=1,
            borderPadding=20,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(title, title_with_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Date and info
        date_str = datetime.datetime.now().strftime("%B %d, %Y")
        elements.append(Paragraph(f"Generated on {date_str}", self.caption_style))
        elements.append(Spacer(1, 0.25*inch))
        elements.append(Paragraph("AI-Powered Analysis", self.subsection_style))
        
        elements.append(PageBreak())
        return elements

    def generate_chart(self, chart, df):
        # Set professional style for plots
        plt.style.use('bmh')  # Using a built-in matplotlib style
        
        fig, ax = plt.subplots(figsize=(10, 6))
        chart_type = chart.get("chart_type")
        x_column = chart.get("x_column")
        y_column = chart.get("y_column")
        
        try:
            if chart_type == "scatter":
                ax.scatter(df[x_column], df[y_column], alpha=0.6)
            elif chart_type == "bar":
                df_grouped = df.groupby(x_column)[y_column].mean()
                ax.bar(df_grouped.index, df_grouped.values, color='#3949AB', alpha=0.7)
            elif chart_type == "line":
                ax.plot(df[x_column], df[y_column], color='#303F9F', linewidth=2)
            elif chart_type == "pie":
                df_grouped = df.groupby(x_column)[y_column].sum()
                ax.pie(df_grouped.values, labels=df_grouped.index, autopct='%1.1f%%')
            elif chart_type == "histogram":
                ax.hist(df[y_column], bins=30, color='#3949AB', alpha=0.7)
            
            # Enhance the plot appearance
            ax.set_title(f"{chart_type.title()} Chart: {x_column} vs {y_column}", 
                        pad=20, fontsize=12, fontweight='bold')
            ax.set_xlabel(x_column, fontsize=10)
            ax.set_ylabel(y_column, fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Rotate x-axis labels if needed
            if chart_type in ["bar"]:
                plt.xticks(rotation=45, ha='right')
            
            plt.tight_layout()
            
            # Save to buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            return img_buffer
        except Exception as e:
            print(f"Error generating chart: {e}")
            plt.close()
            return None

    def create_table_style(self):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Reduced font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),  # Reduced font size
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ])

    def format_large_tables(self, df, max_rows_per_page=25):
        """Handle large dataframes by splitting them into multiple tables"""
        table_elements = []
        total_rows = len(df)
        
        # Calculate available width
        page_width = letter[0] - 144  # Letter width minus margins
        num_columns = len(df.columns) + 1  # +1 for index
        col_width = page_width / num_columns
        
        # Format data with proper width constraints
        column_widths = [col_width] * num_columns
        
        for start_idx in range(0, total_rows, max_rows_per_page):
            end_idx = min(start_idx + max_rows_per_page, total_rows)
            
            # Create subset of data
            df_subset = df.iloc[start_idx:end_idx]
            
            # Convert to table data
            table_data = [['Index'] + list(df_subset.columns)]
            for idx, row in df_subset.iterrows():
                table_data.append([str(idx)] + [str(val) for val in row.values])
            
            # Create table with calculated widths
            table = Table(table_data, repeatRows=1, colWidths=column_widths)
            table.setStyle(self.create_table_style())
            
            table_elements.append(table)
            
            # Add page break if not the last table
            if end_idx < total_rows:
                table_elements.append(PageBreak())
        
        return table_elements

    def parse_markdown_table(self, markdown_text):
        # Find tables in markdown
        table_pattern = r'\|.*\|[\r\n]\|[-|\s]*\|[\r\n](\|.*\|[\r\n])*'
        tables = re.finditer(table_pattern, markdown_text, re.MULTILINE)
        
        elements = []
        for table_match in tables:
            table_str = table_match.group(0)
            # Split into rows and clean up
            rows = [row.strip() for row in table_str.split('\n') if row.strip()]
            if len(rows) < 3:  # Need header, separator, and at least one data row
                continue
                
            # Process rows into data
            header = [cell.strip() for cell in rows[0].split('|')[1:-1]]
            data_rows = []
            for row in rows[2:]:  # Skip separator row
                data_rows.append([cell.strip() for cell in row.split('|')[1:-1]])
                
            # Create Table
            table_data = [header] + data_rows
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))
            
        return elements

    def markdown_to_paragraphs(self, markdown_text):
        elements = []
        
        # Split content by tables
        parts = re.split(r'(\|.*\|[\r\n]\|[-|\s]*\|[\r\n](?:\|.*\|[\r\n])*)', markdown_text)
        
        for part in parts:
            if part.strip().startswith('|'):
                # Handle tables
                elements.extend(self.parse_markdown_table(part))
            else:
                # Handle regular markdown
                html = markdown.markdown(part)
                paragraphs = html.split('\n')
                for p in paragraphs:
                    if p.strip():
                        if p.startswith('<h1>'):
                            style = self.title_style
                            p = p.replace('<h1>', '').replace('</h1>', '')
                        elif p.startswith('<h2>'):
                            style = self.section_style
                            p = p.replace('<h2>', '').replace('</h2>', '')
                        else:
                            style = self.body_style
                            p = p.replace('<p>', '').replace('</p>', '')
                        elements.append(Paragraph(p, style))
                        elements.append(Spacer(1, 8))
        
        return elements

    def create_complete_report(self, context_response, report_response, df, figures, output_path, report_title):
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=50,  # Reduced margins
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )
            elements = []

            # Add cover page
            elements.extend(self.create_cover_page(report_title))

            # Table of Contents with styling
            toc_style = ParagraphStyle(
                'TOC',
                parent=self.body_style,
                leftIndent=20,
                spaceBefore=6,
                spaceAfter=6
            )
            elements.append(Paragraph("Contents", self.section_style))
            toc_items = ["1. Context Analysis", "2. Detailed Analysis", "3. Data Summary", "4. Data Visualizations"]
            for item in toc_items:
                elements.append(Paragraph(f"• {item}", toc_style))
            elements.append(PageBreak())

            # Sections with compact spacing
            sections = [
                ("1. Context Analysis", context_response),
                ("2. Detailed Analysis", report_response)
            ]
            
            for title, content in sections:
                elements.append(Paragraph(title, self.section_style))
                elements.extend(self.markdown_to_paragraphs(content))
                elements.append(Spacer(1, 12))
                elements.append(PageBreak())

            # Data Summary section
            elements.append(Paragraph("3. Data Summary", self.section_style))
            summary_data = df.describe().round(2)
            summary_elements = self.format_large_tables(summary_data, max_rows_per_page=30)
            elements.extend(summary_elements)
            
            # Sample data with compact display
            elements.append(Paragraph("Sample Data", self.subsection_style))
            sample_data = df.head(30)
            sample_elements = self.format_large_tables(sample_data, max_rows_per_page=30)
            elements.extend(sample_elements)
            elements.append(PageBreak())

            # Visualizations section with optimized layout
            elements.append(Paragraph("4. Data Visualizations", self.section_style))
            for i, chart in enumerate(figures, 1):
                chart_title = f"Figure {i}: {chart.get('chart_type').title()} Chart"
                elements.append(Paragraph(chart_title, self.subsection_style))
                
                img_buffer = self.generate_chart(chart, df)
                if img_buffer:
                    img = Image(img_buffer)
                    img.drawHeight = 3.5 * inch  # Slightly reduced size
                    img.drawWidth = 6 * inch
                    elements.append(img)
                
                elements.append(Paragraph(chart.get('reason'), self.caption_style))
                elements.append(Spacer(1, 12))
                
                # Add page break only if needed
                if i % 2 == 0 and i < len(figures):
                    elements.append(PageBreak())

            # Build PDF
            doc.build(elements)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False