from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder='/home/cristian/Documents/Università/Machine_Learning/Dataset')

@app.route('/')
def index():
    # List all CSV files in the directory and its subdirectories
    files_dict = {}
    for dirpath, _, filenames in os.walk(app.static_folder):
        for f in filenames:
            if f.endswith('.csv'):
                file_base_name = os.path.basename(f)
                if dirpath not in files_dict:
                    files_dict[dirpath] = []
                files_dict[dirpath].append((file_base_name, os.path.join(dirpath, f)))
    return render_template('index.html', files_dict=files_dict)


@app.route('/view/<path:filename>/<int:page>/<int:rows_per_page>')
def view_file(filename, page, rows_per_page):
    # Calculate the row numbers to display
    start = (page - 1) * rows_per_page
    end = start + rows_per_page
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv("/"+filename, nrows=end)
    # Get a subset of the DataFrame
    subset = df.iloc[start:end]
    # Convert the DataFrame to an HTML table
    table = subset.to_html()
    return render_template('view.html', table=table, filename=filename, page=page, rows_per_page=rows_per_page)



if __name__ == "__main__":
    app.run(debug=True)
