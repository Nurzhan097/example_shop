$(document).ready(function () {

    // Get cookie 
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    // Send ajax request
    function ajax_request(data, url, type, cache, success, error) {
        // AJAX //
        $.ajax({
            headers: {
                // 'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            url: url,
            dataType: 'json',
            data: data,
            type: type,
            cache: cache,
            success: success,
            error: error,
        });
        // END AJAX //
    }


    // Обновление списка продуктов в корзине и значение колличества
    function update_product_in_busket(data) {
        console.log('OK');
        // Обновление кол-ва продуктов в корзине
        $("#basket_total_nmb").text(data.products_total_nmb);
        $("#basket_total_nmb1").text('(' + data.products_total_nmb + ')');

        // Обновление продуктов в корзине
        $('.shopping_cart ul').html('');
        $.each(data.products_in_basket_list, function (i, v) {
            $('.shopping_cart ul').append(
                '<li class="list-group">' +
                '<div class="pl-thumb">' +
                '<img src="'+
                v.image_url +
                '" alt="">' +
                '</div>' +
                '<a href="' +
                v.url +
                '">' +
                v.title +
                '</a>' +
                v.nmb +
                'x' +
                v.price_per_item +
                '=' +
                v.total_amount +
                '<a class="delete-item" href="/orders/basket/delete/" data-product_id="' +
                v.id +
                '">' +
                'X' +
                '</a>' +
                '</li>'
            );
            // console.log(v.image_url);
        });
        console.log(data.message);
    }


    // Сообщение об ошибке для ajax
    function error_message() {
        console.log('Error');
    }

    // Добавление продукта в корзину
    // Форма
    var form = $('#form_bying_product');
    form.on('submit', function (e) {
        e.preventDefault();

        //Get product parameters
        var nmb = $('#number').val();
        var submit_btn = $('#submit_btn');
        var product_id = submit_btn.data("product_id");
        var product_name = submit_btn.data("product_name");
        var product_price = submit_btn.data("product_price");

        //for debug
        // console.log(nmb);
        // console.log(submit_btn);
        // console.log(product_id);
        // console.log(product_name);
        // console.log(product_price);

        // Parameters for ajax:
        // data
        data = {
            // "csrf_token": csrf_token,
            "nmb": nmb,
            // "submit_btn": submit_btn,
            "product_id": product_id,
            "product_name": product_name,
            "product_price": product_price,
        };
        //url
        var url = form.attr("action");
        //type
        var type = "POST";
        //cache
        var cache = true;
        // ajax request
        ajax_request(data, url, type, cache, update_product_in_busket, error_message);
    })


    // Удаление продукта из корзины
    $(document).on('click', '.delete-item', function (e) {
        e.preventDefault();

        var product_id = $(this).data("product_id");
        // Parameters for ajax:
        // data
        data = {
            "product_id": product_id,
        };
        //url
        var url = '/orders/basket/delete/';
        //type
        var type = "POST";
        //cache
        var cache = true;
        // ajax request
        ajax_request(data, url, type, cache, update_product_in_busket, error_message);

        // $(this).closest('li').remove();
    });

    // подсчет стоимости товара
    function calculationBasketAmount(){
        var total_order_amount = 0;
        // var total_order_amount1 = 0;
        // var total_product_in_basket_amount = 

        // Подсчет конечной цены заказа
        $(".checkout-cart .total-product-in-basket-amount").each(function(){
            total_order_amount += parseInt($(this).text());
            // console.log('total_order_amount '+$(this).text());
        });
        // total_order_amount1 += parseInt($(".total_product_in_basket_amount").each().text());
        // console.log('total_order_amount '+total_order_amount);
        $('#total_order_amount').text(total_order_amount)
        // console.log(total_order_amount1);
    }
    calculationBasketAmount();
    
    $(document).on('change', 'input.product-in-basket_nmb', function(){
        var current_nmb =parseInt( $(this).val());

        var current_li = $(this).closest('li');

        var currnent_price = parseInt(current_li.find('.product-price').text());
        var total_product_in_basket_amount = current_nmb * currnent_price;
        
        // console.log('current_nmb '+current_nmb)
        // console.log('current_li '+current_li)
        // console.log('currnent_price '+currnent_price)
        // console.log('total_product_in_basket_amount '+total_product_in_basket_amount)

        current_li.find('.total-product-in-basket-amount').text(total_product_in_basket_amount);
        calculationBasketAmount();
    });

})