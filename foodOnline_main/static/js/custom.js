$(document).ready(function(){
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
                try {
                    $('#cart-counter').html(response.cart_counter['cart_counter']);
                    $('#quantity-'+food_id).html(response.quantity);
                } catch(error) {
                    console.error('An error occurred while updating the cart counter:', error);
                }
            }
        })
    })

    // Placing the quantity in the quantity place
    $('.item_quantity').each(function(){
        var id = $(this).attr('id');
        var quantity = $(this).attr('data-quantity');
        console.log(id, quantity);
        $('#'+ id ).html(quantity)
    })
})