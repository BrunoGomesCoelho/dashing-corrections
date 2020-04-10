import os
import dash
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, State, Output

from pathlib import Path


IDX = None 
names = []
html_content = []

for folder in [x for x in Path(".").iterdir() if x.is_dir()]:
    f = list(folder.iterdir())[0]
    base_name, extension = str(f).split(".")

    if extension not in ["html", "ipynb"]:
        print(f"WRONG FORMAT {extension} for {base_name}")
        continue

    if extension == "ipynb":
        cmd = f"jupyter nbconvert '{str(f)}'"
        os.system(cmd)
    output_name = base_name + ".html"

    with open(output_name, "r") as f:
        html_content.append(f.read())
    names.append(str(f.name))

with open("processed.txt", "w") as f:
    f.write("\n".join(names))


app = dash.Dash('')

app.scripts.config.serve_locally = True

app.layout = html.Div([
    html.Button('Next', id='button'),
    html.Div('Student name:', id='name'),
    html.Div("hi", id="inside"),
])


@app.callback([Output('inside', 'children'),
               Output('name', 'children')],
              [Input('button', 'n_clicks')])
def update_output(n_clicks):
    global IDX, names
    if n_clicks is None:
        IDX = 0
        return "Click Next to start", ""

    if IDX >= len(html_content):
        return "All done!", ""

    name = f"Student name: {names[IDX]}"
    content = html_content[IDX]
    IDX += 1
    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(content), name



if __name__ == '__main__':
    app.run_server(debug=True)
