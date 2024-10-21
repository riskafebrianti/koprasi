odoo.define('custom_koprasi.models', function(require) {
    'use strict';

    var { Orderline } = require('point_of_sale.models');
    var Registries = require('point_of_sale.Registries');

    const CustomOrder = (Orderline) => class CustomOrder extends Orderline{
        export_for_printing(){
            var result = super.export_for_printing(...arguments);
            result.digital = this.get_product().digital;
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
