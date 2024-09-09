odoo.define('custom_pos.PaymentScreen', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const CustomPaymentScreen = (PaymentScreen) => class extends PaymentScreen {
        async validateOrder(isForceValidate) {
            const order = this.currentOrder;
            const partner = order.get_partner();
            const paymentLines = order.get_paymentlines();
            const cashMethod = this.env.pos.payment_methods.find(method => method.cash_journal === true);

            // Check if the payment method is 'cash' and the customer has more than 5 orders
            if (partner && partner.total_orders >= 5 && paymentLines.some(line => line.payment_method.id === cashMethod.id)) {
                // Show error popup and prevent validation
                this.showPopup('ErrorPopup', {
                    title: 'Order Limit Exceeded',
                    body: 'This customer has more than 5 orders and cannot pay with cash.',
                });
                return;  // Stop the validation if error
            }

            // Proceed with the normal flow if no error
            super.validateOrder(isForceValidate);
        }
    };

    Registries.Component.extend(PaymentScreen, CustomPaymentScreen);
    return PaymentScreen;
});
