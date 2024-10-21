odoo.define('custom_koprasi.PaymentScreen', function (require) {
    "use strict";

    var Gui = require('point_of_sale.Gui');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    // const { _lt} = require('@web/core.l10n/translation');

    var core = require('web.core');
    var _t = core._t;
    
    const PaymenrScreenCredit = (PaymentScreen) =>
        class extends PaymentScreen{
            async validateOrder(isForceValidate){

                const order = this.currentOrder;
                const partner = order.get_partner();
                const paymentLines = order.get_paymentlines();
                const cashMethod = this.env.pos.payment_methods.find(method => method.id === '3');
                let idrFormat = new Intl.NumberFormat('id-ID', {
                    style: 'currency',
                    currency: 'IDR',
                    minimumFractionDigits: 0,  // No decimal places for IDR
                });

                // console.log(typeof(paymentLines))
                // console.log(idrFormat)
                // console.log(paymentLines[0]['name'])
                // console.log(paymentLines)
                // console.log(partner,'doinjdsanso')
                // console.log(this.env.pos.payment_methods,'doinjdsanso')

                if (paymentLines[0]['name'] == 'Customer Account' && paymentLines[0]['amount'] + partner['credit_limit'] > partner['limit']){
                    const keterangan = "Total Limit " + partner['name'] + " adalah " + idrFormat.format(partner['limit'])
                    this.showPopup('ErrorPopup',{
                        title : this.env._t('Pembelian Lebih dari Limit'),
                        body :
                            this.env._t(keterangan),
                    });
                    return 
                }
                super.validateOrder(isForceValidate);   
            }
                       
        };

        Registries.Component.extend(PaymentScreen, PaymenrScreenCredit);
        return PaymenrScreenCredit;

});