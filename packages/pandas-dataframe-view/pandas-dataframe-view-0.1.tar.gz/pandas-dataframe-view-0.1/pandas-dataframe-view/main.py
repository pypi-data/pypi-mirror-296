import pandas as pd
import webbrowser
import tempfile

def view_df(df: pd.DataFrame):
    """
    Converts the given DataFrame to an HTML file with auto-adjusted column widths
    and opens it in the default web browser.
    
    Parameters:
    df (pd.DataFrame): The pandas DataFrame to display.
    """
    # Define custom CSS for column width adjustment
    css = """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 8px;
        text-align: left;
        white-space: nowrap;
    }
    th {
        background-color: #f2f2f2;
    }
    </style>
    """
    
    # Convert DataFrame to HTML and add the CSS
    html = df.to_html()
    html_with_css = css + html
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as temp_file:
        # Write the HTML with CSS to the temporary file
        temp_file.write(html_with_css)
        temp_file.flush()  # Ensure all data is written
        
        # Open the HTML file in the default web browser
        webbrowser.open('file://' + temp_file.name)

# Example usage
if __name__ == "__main__":
    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Occupation': ['Engineer', 'Doctor', 'Artist'],
            'Location': ['New York', 'Los Angeles', 'Chicago']}
    df = pd.DataFrame(data)
    view_df(df)
