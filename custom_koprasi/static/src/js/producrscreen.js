// BiProductScreen js
odoo.define('custom_koprasi.productScreen', function(require) {
	"use strict";

	const Registries = require('point_of_sale.Registries');
	const ProductScreen = require('point_of_sale.ProductScreen');
	var rpc = require('web.rpc')

	const BiProductScreen = (ProductScreen) =>
		class extends ProductScreen {
			super() {
				super.setup();
			}
			async _onClickPay() {
				let call_super = true;
				const order = this.currentOrder;
				var lines = order.get_orderlines();
				if (this.env.pos.res_setting['stock_from'] == 'current_warehouse') {
                    if (this.env.pos.res_setting['stock_type'] == 'on_hand') {
                        let stopValidation = false;
                        // lines.forEach(async(line) => {
                        for (const line of lines)  {
                            const item_quantity = line.quantity
                            const on_hand_qty = line.product.on_hand
                            console.log(line.product.display_name,"halooo")
                            const available_qty = line.product.available
                            // if 
                            if (on_hand_qty < item_quantity){
                                // var item_quantity = line.quantity
                                // var on_hand_qty = line.product.on_hand
                                // var new_qty = on_hand_qty + item_quantity
                                // line.product.on_hand = new_qty

                                const body = _.str.sprintf(this.env._t('%s is Out Of Stock'), );
                                const bodyy = "Total Limit " + line.product
                                await this.showPopup('ErrorPopup', {
                                    title: this.env._t("Cek Stok"),
                                    body :
                                    this.env._t(line.product.display_name),
                                    // break;
                                });
                                
                                return
                            }
                          
                        }
                    } 
                }
				// if(this.env.pos.get_order()){
				// 	console.log("this.env.pos.get_order()")

				
				if(call_super){
					super._onClickPay();
				}
				
			}
		};

	Registries.Component.extend(ProductScreen, BiProductScreen);

	return ProductScreen;

});
