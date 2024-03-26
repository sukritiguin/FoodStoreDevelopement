$(document).ready(function(){
    // Add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        food_url = $(this).attr('data-url');

        data = {
            food_id:food_id,
        }

        $.ajax({
            type: 'GET',
            url:food_url,
            data: data,
            success: function(response){
                if(response.status == 'Failed'){
                    swal("Something went wrong", response.message, "warning");
                }else if(response.status == 'login_required'){
                    swal("Please Login!", "You need to login first.", "warning").then(function(){
                        window.location = '/login';
                    });
                }else{
                    $('#cart-counter').html(response.cart_counter['cart_counter']);
                    $('#quantity-'+food_id).html(response.quantity);
                }
            }
        })
    })

    // Placing the quantity in the quantity place
    $('.item_quantity').each(function(){
        var id = $(this).attr('id');
        var quantity = $(this).attr('data-quantity');
        $('#'+ id ).html(quantity)
    })


    // Decrease Cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        food_url = $(this).attr('data-url');

        data = {
            food_id:food_id,
        }

        $.ajax({
            type: 'GET',
            url:food_url,
            data: data,
            success: function(response){
                console.log(response);
                if(response.status == 'Failed'){
                    swal("Something went wrong", response.message, "warning");
                }else if(response.status == 'login_required'){
                    swal("Please Login!", "You need to login first.", "warning").then(function(){
                        window.location = '/login';
                    });
                }else{
                    $('#cart-counter').html(response.cart_counter['cart_counter']);
                    $('#quantity-'+food_id).html(response.quantity);
                }
            }
        })
    })
})