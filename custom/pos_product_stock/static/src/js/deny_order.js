odoo.define('pos_product_stock.Custom', function(require) {
    'use strict';
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const order = (ProductScreen) => class extends ProductScreen {
        //we extends ProductScreen to super _clickproduct function.
        async _clickProduct(event) {
            var self = this;
            let order = this.env.pos.get_order();
            let lines = order.get_orderlines();
            console.log(lines,'ena')
            if (event.detail.detailed_type == 'product') {
                if (this.env.pos.res_setting['stock_from'] == 'all_warehouse') {
                    console.log(event,'ena1')
                    if (this.env.pos.res_setting['stock_type'] == 'on_hand') {
                        console.log(event,'ena2')
                        if (event.detail.qty_available <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            }); //shows error pop up as condition satisfies.
                        } else {
                            super._clickProduct(event);
                        }
                    } else if (this.env.pos.res_setting['stock_type'] == 'outgoing_qty') {
                        if (event.detail.outgoing_qty <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            });
                        } else {
                            super._clickProduct(event);
                        }
                    } else if (this.env.pos.res_setting['stock_type'] == 'incoming_qty') {
                        if (event.detail.incoming_qty <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            });
                        } else {
                            super._clickProduct(event);
                        }
                    } else if (this.env.pos.res_setting['stock_type'] == 'available_qty') {
                        if (event.detail.available_product <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            });
                        } else {
                            super._clickProduct(event);
                        }
                    }
                } else if (this.env.pos.res_setting['stock_from'] == 'current_warehouse') {

                    if (this.env.pos.res_setting['stock_type'] == 'on_hand') {
                        console.log(["lines"].quantity,"bisaa dong")

                        for (const line of lines)  {
                            const item_quantity = line.quantity
                            const on_hand_qty = line.product.on_hand
                            console.log(line.product.available,"halooo")
                            console.log(on_hand_qty,"oh")
                            console.log(item_quantity,"iq")
                            const available_qty = line.product.available
                            const tes = on_hand_qty < item_quantity
                            console.log(tes,"cnd")
                            // if 
                            if (on_hand_qty < item_quantity){
                                

                                const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), );
                                const bodyy = "Total Limit " + line.product
                                await this.showPopup('ErrorPopup', {
                                    title: this.env._t("Barang Kurang Dari Stok"),
                                    body :
                                    this.env._t(line.product.display_name),
                                    // break;
                                });
                               
                                return
                            }
                            
                        }

                        console.log(lines.name,'ena')
                        if (event.detail.on_hand <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            });
                        } else {
                            super._clickProduct(event);
                        }
                    } else if (this.env.pos.res_setting['stock_type'] == 'outgoing_qty') {
                        if (event.detail.outgoing <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            });
                        } else {
                            super._clickProduct(event);
                        }
                    } else if (this.env.pos.res_setting['stock_type'] == 'incoming_qty') {
                        if (event.detail.incoming <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            });
                        } else {
                            super._clickProduct(event);
                        }
                    } else if (this.env.pos.res_setting['stock_type'] == 'available_qty') {
                        console.log(event['detail'])
                        
                       
                        if (event.detail.available <= event.detail.deny) {
                            const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Deny Order'),
                                body
                            });
                        } else if (event['detail']['pos']['orders'][0]['orderlines'].length > 0) {
                            if (event.detail.available <= event.detail.pos.orders[0].orderlines[0].quantity){
                                const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), event.detail.display_name);
                                await this.showPopup('ErrorPopup', {
                                    title: this.env._t('Deny Order'),
                                    body
                                });
                            }
                        } else {
                            super._clickProduct(event);
                        }
                    }
                }
            } else {
                super._clickProduct(event);
            }
        }
    }
    Registries.Component.extend(ProductScreen, order);
});
