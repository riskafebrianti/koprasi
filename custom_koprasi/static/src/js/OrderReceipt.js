odoo.define('custom_koprasi.Orderline', function(require) {
    'use strict';

    var { Orderline } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrder = (Orderline) => class CustomOrder extends Orderline{
        export_for_printing(){
            const result = super.export_for_printing(...arguments);
            const product = this.get_product();
            // console.log(result,'doinjdsanso')
            console.log(product,'doinjdsanso')
            result.digital = product.digital;
            result.digital_inv = product.digital_inv;
            return result;
        }
    }
    

    Registries.Model.extend(Orderline, CustomOrder);

    });

  
// odoo.define('custom_koprasi.receipt', function(require){
//     "use strict";
//     var models = require('point_of_sale.models');
//     models.load_fields('product.template', 'product_grade_id');
//     var _super_orderline = models.Orderline.prototype;
//     models.Orderline = models.Orderline.extend({
//         export_for_printing: function(){
//             var line = _super_orderline.export_for_printing.apply(this, arguments);
//             line.new_field = this.get_product().digital;
//             return line;
//         }
//     });
// });
