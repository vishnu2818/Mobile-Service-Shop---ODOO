# Mobile-Service-Shop---ODOO
ODOO Module Creation Mobile Service Shop 

TASK-1
Create a module called Mobile service shop.
Mobile service shop module should have following field.
1.Customer name
2.Mobile OS type - selection field -  (Android,Basic,OS)
3.Mobile company - Many2one eg--> Nokia,vivo,oppo
4.Mobile complaint description.
5.Mobile service line - One2many
  5.1 Product
  5.2 Qty
  5.3 Unit price
  5.4 Subtotal
6. Total
7.Damaged spare parts --> Many2many eg-->Display,speaker.
8.Simple q web report --> Mobile service slip
9.State should need to add --> draft,confirm,cancel.

10. Company  and user field need to get current company and user.

TASK-2
1. Add confirm button in your form, Sequence should be generate after confirmation. eg-->(Mob0001)
2. Graph,Pivot,Calendar,search view to be added.

3. Add a related field  phone of customer in sale order. --> Study related field attributes in Odoo technical documentation(Place a field below customer field).
4. In Mobile service customized module, Delete can be done only in draft state.
5. Python date conversion --> date-time to string etc... --> Refer w3 school.

TASK-3
1. In your module, If Product was not chosen then warning need to raise. To aware the user product is not selected.
2. All Fields should be read only in confirm stage.

3. Add Cancel and Reset to draft button.

4. Kindly Add a new description field in Line item.If a product is chosen the Product name and internal reference need to update in the description field.
5. Approve mechanism
    4.1 --> sales User can create Mobile service form.
    4.2 --> Sales manager need to Approve Mobile service form before confirm.
    (Create a new user call sales person and Sales Manager --> Refer odoo functional documentation.)
