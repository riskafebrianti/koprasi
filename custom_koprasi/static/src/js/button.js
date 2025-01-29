odoo.define('custom_koprasi.button', function(require) {
    'use strict';
      const { Gui } = require('point_of_sale.Gui');
      const PosComponent = require('point_of_sale.PosComponent');
      const { identifyError } = require('point_of_sale.utils');
      const ProductScreen = require('point_of_sale.ProductScreen');
      const { useListener } = require("@web/core/utils/hooks");
      const Registries = require('point_of_sale.Registries');
      const PaymentScreen = require('point_of_sale.PaymentScreen');
      const rpc = require('web.rpc');
      const models = require('point_of_sale.models');
    
    

      class CustomDemoButtons extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        // constructor() {
        //     super(...arguments);
        //     useListener('add-order-note', this.onClick);
        // }
        async onClick() {
            const order = this.env.pos.get_order();
            if (!order) return;
            const {confirmed, payload:inputNote } = await this.showPopup('TextAreaPopup', {
                title: this.env._t('Add Customer Note'),
                startingValue: order.note || '',
            });
            
            if (confirmed) {
                order.addOrderNote(inputNote);
            }
        }
    }
                // this.env.pos.get_order().note = payload; // Simpan catatan pada order
                // console.log(this.env.pos.get_order())
                // console.log('Catatannkkk:', order.paymentlines[0]);

                // syncOrderResult = await this.env.pos.push_single_order(this.currentOrder);
                //  = note
                // this.env.pos.get_order() = order.note
                // this.env.pos.get_order() = order.note;
                // this.env.pos.get_order().name = order.paymentlines[0].name +' ' +order.note
                
                // const order = this.env.pos.get_order();
                // const yourData = order.your_field; // Ambil data dari POS

                // this.rpc({
                //     model: 'pos.order',
                //     method: '_order_fields',
                //     args: [[{
                //         your_field: order.note,
                //         // Tambahkan data lain seperti lines, partner, dll.
                //     }]],
                // }).then((result) => {
                //     console.log('Data saved to backend:', result);
                // }); 
                
    
            
    CustomDemoButtons.template = 'CustomDemoButtons';

      ProductScreen.addControlButton({
          component: CustomDemoButtons,
       
      });
     
      Registries.Component.add(CustomDemoButtons);
      return CustomDemoButtons;
    });
    

