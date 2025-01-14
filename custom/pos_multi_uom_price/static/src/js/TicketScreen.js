/* ehuerta _at_ ixer.mx */

odoo.define('pos_multi_uom_price.TicketScreen', function (require) {
    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');

    const PosUOMTicketScreen = (TicketScreen) =>
        class extends TicketScreen {
            //@override
        _getToRefundDetail(orderline) {
            if (orderline.id in this.env.pos.toRefundLines) {
                return this.env.pos.toRefundLines[orderline.id];
            } else {
                const partner = orderline.order.get_partner();
                const orderPartnerId = partner ? partner.id : false;
                const newToRefundDetail = {
                    qty: 0,
                    orderline: {
                        id: orderline.id,
                        productId: orderline.product.id,
                        price: orderline.price,
                        qty: orderline.quantity,
                        refundedQty: orderline.refunded_qty,
                        orderUid: orderline.order.uid,
                        orderBackendId: orderline.order.backendId,
                        orderPartnerId,
                        tax_ids: orderline.get_taxes().map(tax => tax.id),
                        discount: orderline.discount,
                        product_uom_id: orderline.product_uom_id,
                    },
                    destinationOrderUid: false,
                };
                this.env.pos.toRefundLines[orderline.id] = newToRefundDetail;
                return newToRefundDetail;
            }
        }
        _prepareRefundOrderlineOptions(toRefundDetail) {
            const { qty, orderline } = toRefundDetail;
            return {
                quantity: -qty,
                price: orderline.price,
                extras: { price_manually_set: true },
                merge: false,
                refunded_orderline_id: orderline.id,
                tax_ids: orderline.tax_ids,
                discount: orderline.discount,
                product_uom_id: orderline.product_uom_id,
            }
        }

            };

    Registries.Component.extend(TicketScreen, PosUOMTicketScreen);

    return { TicketScreen };
});

