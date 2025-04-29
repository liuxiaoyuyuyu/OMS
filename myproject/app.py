from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('data.csv')  # Replace with your CSV filename

@app.route('/api/v1/fills/')
def list_fills():
    filtered_df = df.copy()

    # Parse query parameters like filter[fill_number][EQ]=10530
    for param, value in request.args.items():
        if param.startswith('filter[') and param.endswith(']'):
            try:
                field_and_op = param[len('filter['):-1]  # remove 'filter[' and ']'
                field, op = field_and_op.split('][')     # get field and operator
                if field not in df.columns:
                    continue  # skip unknown fields

                val = float(value) if df[field].dtype.kind in 'if' else value
                if op == 'EQ':
                    filtered_df = filtered_df[filtered_df[field] == val]
                elif op == 'GT':
                    filtered_df = filtered_df[filtered_df[field] > val]
                elif op == 'LT':
                    filtered_df = filtered_df[filtered_df[field] < val]
                elif op == 'GTE':
                    filtered_df = filtered_df[filtered_df[field] >= val]
                elif op == 'LTE':
                    filtered_df = filtered_df[filtered_df[field] <= val]
            except Exception as e:
                print(f"Error parsing filter: {param} = {value} ({e})")

    data = [
        {
            "id": str(row["fill_number"]),
            "type": "fills",
            "attributes": {
                k: row[k] for k in df.columns if k != "fill_number"
            }
        } for _, row in filtered_df.iterrows()
    ]
    return jsonify({"data": data})

# Helper to format a row as JSON:API
def format_fill(row):
    return {
        "data": {
            "id": str(row["fill_number"]),
            "type": "fills",
            "attributes": row.drop("fill_number").to_dict()
        }
    }

@app.route('/api/v1/fills/<fill_number>', methods=['GET'])
def get_fill(fill_number):
    try:
        fill_number = int(fill_number)
    except ValueError:
        abort(400, description="Invalid fill_number. Must be an integer.")

    fill = df[df["fill_number"] == fill_number]

    if fill.empty:
        abort(404, description="Fill not found.")

    row = fill.iloc[0]
    return jsonify(format_fill(row))

if __name__ == '__main__':
    app.run(debug=True)


