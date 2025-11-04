$('.plus-cart').click(function () {
    console.log('Plus button clicked');
    var $btn = $(this);
    $btn.prop('disabled', true); // Disable button during request

    var id = $btn.attr('pid').toString();
    var quantity = this.parentNode.children[2];

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            cart_id: id
        },
        success: function (data) {
            console.log('Success:', data);
            // Update quantity in both places
            quantity.innerText = data.quantity;
            $(`#quantity${id}`).text(data.quantity);

            // Update totals with animation
            $('#amount_tt').fadeOut(200, function () {
                $(this).text(data.amount).fadeIn(200);
            });
            $('#totalamount').fadeOut(200, function () {
                $(this).text(data.total).fadeIn(200);
            });
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
            alert('Failed to update quantity. Please try again.');
        },
        complete: function () {
            $btn.prop('disabled', false); // Re-enable button
        }
    });
})


$('.minus-cart').click(function () {
    console.log('Minus button clicked');
    var $btn = $(this);
    $btn.prop('disabled', true); // Disable button during request

    var id = $btn.attr('pid').toString();
    var quantity = this.parentNode.children[2];

    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: {
            cart_id: id
        },
        success: function (data) {
            console.log('Success:', data);
            // Update quantity in both places
            quantity.innerText = data.quantity;
            $(`#quantity${id}`).text(data.quantity);

            // Update totals with animation
            $('#amount_tt').fadeOut(200, function () {
                $(this).text(data.amount).fadeIn(200);
            });
            $('#totalamount').fadeOut(200, function () {
                $(this).text(data.total).fadeIn(200);
            });
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
            alert('Failed to update quantity. Please try again.');
        },
        complete: function () {
            $btn.prop('disabled', false); // Re-enable button
        }
    });
})


$('.remove-cart').click(function () {

    var id = $(this).attr('pid').toString()

    var to_remove = this.parentNode.parentNode.parentNode.parentNode

    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: {
            cart_id: id
        },

        success: function (data) {
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
            to_remove.remove()
        }
    })


})
