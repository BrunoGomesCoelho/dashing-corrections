import os
import dash
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, State, Output

from pathlib import Path


IDX = None
names = []
html_content = []
all_files = [x for x in Path(".").iterdir() if x.is_dir()]
all_files.sort()


def print_error(student, msg):
    print(f"Student {student}: {msg}")


for folder in all_files:
    # TODO: This assumes the students only submit 1 file as a JN, which is
    # frequently not the case
    for f in list(folder.iterdir()):
        splits = str(f).split(".")

        # Students make dumb mistakes/send unexpected files
        if len(splits) > 2:
            print_error(folder, "file with more than one '.' in it 🤷")
            continue
        elif len(splits) < 2:
            print_error(folder, "file with no dots? 🤔")
            continue
        else:
            base_name, extension = splits

        # We only process ipynb but since we may run the same code more than once,
        # we also allow the already processed html files
        if extension not in ["html", "ipynb"]:
            print(f"WRONG FORMAT {extension} for {base_name}")
            continue

        # Convert and save file
        if extension == "ipynb":
            cmd = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True "  \
                   + "--ClearMetadataPreprocessor.enabled=True " \
                   + f"--to html '{str(f)}'"
            os.system(cmd)
        output_name = base_name + ".html"

        try:
            with open(output_name, "r") as f:
                html_content.append(f.read())
                names.append(str(f.name))
        except:
            print(f"ERROR with {str(f)} - {output_name} - Not a notebook?")

# Save a log of processed files
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
    """ Processes the various student files.
    There is certainly a more elogant way of doing it than a global IDX :)
    """
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
