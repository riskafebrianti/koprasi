odoo.define('pos_access_right_hr.CustomOrdrScreen', function(require) {
    'use strict';
       const NumpadWidget = require('point_of_sale.NumpadWidget');
       const Registries = require('point_of_sale.Registries');
       const disablee= NumpadWidget => class extends NumpadWidget {
       //To enable or disable buttons in the NumpadWidget
   
        /**
        * Disable the Qty button on the POS
        */
        
   
        /**
        * Disable the Price button on the POS
        */
        get disable_price() {
            console.log('HALOOO 2')
           // if (this.env.pos.config.module_pos_hr) {
          
            return disable_price 
           // }
           // else { return false;}
       }
   
        /**
        * Disable the Discount button on the POS
        */
     
   
        /**
        * Disable the +/- button on the POS
        */
       
   
        /**
        * Disable the number pad on the POS
        */
      
   
       /**
        * Disable the back button on the POS
        */
      
       };
       Registries.Component.extend(NumpadWidget, disablee);
       return NumpadWidget;
    });
   