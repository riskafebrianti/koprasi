odoo.define('custom_koprasi.hitung', function(require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const PosComponent = require('point_of_sale.PosComponent');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const models = require('point_of_sale.models');
    

    class CustomButtons extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }

        async onClick() {
            const order = this.env.pos.get_order();
            if (!order) return;
            const selectedLine = order.get_selected_orderline();
           
            const { confirmed, payload: inputAmount } = await this.showPopup('NumberPopup', {
                title: 'Enter Amount for Line',
                // startingValue: ,
                startingValue: selectedLine.harga || '',
            });

            if (confirmed) {
                console.log("Amount Set:", inputAmount);
                const formattedAmount = new Intl.NumberFormat('id-ID', { 
                    style: 'currency', 
                    currency: 'IDR' 
                }).format(inputAmount);
                selectedLine.inputHarga(Number(inputAmount))
               
                const bagii = selectedLine.harga / selectedLine.get_quantity() 
                selectedLine.price = bagii

                const harga_dari_bagii = Number(Number(bagii).toFixed(2));
                const quantity = selectedLine.get_quantity();
                const sub_total = harga_dari_bagii * quantity;
               
            
                if (sub_total < inputAmount) {
                    const defaultProductId = "ROUND";  // Ganti dengan ID produk default yang ingin ditambahkan
                    const defaultProduct = Object.values(this.env.pos.db.product_by_id).find(
                        (product) => product.display_name === defaultProductId
                    );
                    const pengurangan = inputAmount - sub_total;
                    // console.log("A", inputAmount);
                    // console.log("B", sub_total);
                
            
                    if (defaultProduct) {
                        order.add_product(defaultProduct, {
                            price: pengurangan, // Harga default
                        });
                       
                    } 
                }
                
                
                // console.log("Amount Set:", formattedAmount);
                // console.log("sup total:", selectedLine.get_price_without_tax() < inputAmount);
                // console.log("qty:", selectedLine.get_quantity());
                // // console.log("hasil kedua:", newProduct);
                // console.log("price Set:", selectedLine.price);
                // console.log("sub total:", selectedLine.get_price_without_tax());
                // console.log("kurangnya :", (inputAmount - sub_total));
                
            }
        }
    }

    CustomButtons.template = 'CustomButtons';

    ProductScreen.addControlButton({
        component: CustomButtons,
     
    });
   
    Registries.Component.add(CustomButtons);
    return CustomButtons;
  });
  