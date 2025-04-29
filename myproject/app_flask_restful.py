from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd

app = Flask(__name__)
api = Api(app)

# Load CSV
df = pd.read_csv('data.csv')

# Allowed filter operations
FILTER_OPERATORS = {
    'EQ': lambda x, y: x == y,
    'NE': lambda x, y: x != y,
    'GT': lambda x, y: x > y,
    'GTE': lambda x, y: x >= y,
    'LT': lambda x, y: x < y,
    'LTE': lambda x, y: x <= y,
}


class FillList(Resource):
    def get(self):
        filtered_df = df.copy()

        # Handle filter queries
        for arg, value in request.args.items():
            if arg.startswith('filter[') and '][' in arg:
                try:
                    col_op = arg[len('filter['):-1]
                    col, op = col_op.split('][')
                    op = op.upper()

                    if op in FILTER_OPERATORS and col in df.columns:
                        try:
                            typed_val = pd.to_numeric(value, errors='ignore')
                            filtered_df = filtered_df[FILTER_OPERATORS[op](filtered_df[col], typed_val)]
                        except Exception:
                            continue
                except Exception:
                    continue

        # Handle sorting
        sort_key = request.args.get('sort')
        if sort_key:
            ascending = not sort_key.startswith('-')
            sort_key = sort_key.lstrip('-')
            if sort_key in df.columns:
                filtered_df = filtered_df.sort_values(by=sort_key, ascending=ascending)

        # Build response
        return {
            'data': [
                {
                    'id': str(row['fill_number']),
                    'type': 'fills',
                    'attributes': row.drop('fill_number').to_dict()
                } for _, row in filtered_df.iterrows()
            ]
        }


class Fill(Resource):
    def get(self, fill_number):
        data = df[df['fill_number'] == fill_number]
        if data.empty:
            return {'errors': [{'detail': 'Fill not found'}]}, 404

        row = data.iloc[0]
        return {
            'data': {
                'id': str(row['fill_number']),
                'type': 'fills',
                'attributes': row.drop('fill_number').to_dict()
            }
        }

api.add_resource(FillList, '/api/v1/fills/')
api.add_resource(Fill, '/api/v1/fills/<int:fill_number>')

if __name__ == '__main__':
    app.run(debug=True)
