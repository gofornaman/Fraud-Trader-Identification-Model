from flask import Flask
from flask_restplus import Api, Resource, fields


app = Flask(__name__)

api = Api(
   app, 
   version='1.0', 
   title='Trader Identifcation Model (TIM)',
   description='Segregating bulk traders from legitimate customers')

ns = api.namespace('namespace_tim', 
   description='')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

# order_count
# isFirstBulk
# linked_to
# no_of_phones_associated
# no_of_address_associated
# promotion

parser = api.parser()
parser.add_argument(
   'order_count', 
   type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'isFirstBulk', 
   type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'linked_to', 
   type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'no_of_phones_associated', 
   type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'no_of_address_associated', 
   type=float, 
   required=True, 
   location='form')

parser.add_argument(
   'promotion', 
   type=float, 
   required=True, 
   location='form')


@ns.route('/')
class CreditApi(Resource):

   @api.doc(parser=parser)
   @api.marshal_with(resource_fields)
   def post(self):
     args = parser.parse_args()
     result = self.get_result(args)

     return result, 201

   def get_result(self, args):
      order_count = args["order_count"]
      isFirstBulk = args["isFirstBulk"]
      linked_to = args["linked_to"]
      no_of_phones_associated = args["no_of_phones_associated"]
      no_of_address_associated = args["no_of_address_associated"]
      promotion = args["promotion"]

      from pandas import DataFrame
      df = DataFrame([[
         order_count,
         isFirstBulk,
         linked_to,
         no_of_phones_associated,
         no_of_address_associated,
         promotion
      ]])

      from sklearn.externals import joblib
      clf = joblib.load('model/nb.pkl');

      result = clf.predict(df)
      if(result[0] == 1.0): 
         result = "Trader" 
      else: 
         result = "Not a trader"

      return {
         "result": result
      }

if __name__ == '__main__':
    app.run(debug=True)
