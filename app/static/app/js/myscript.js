$('#slider1, #slider2, #slider3, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        280:{
            items:2,
            nav:true,
            autoplay:true
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// Ajax code here


// code for increasing the quantity
$('.plus-cart').click(function(){
    let id = $(this).attr("pid").toString();
    let eml = this.parentNode.children[2];
    let amount = document.querySelector('#amount');
    let totalAmount = document.querySelector('#totalamount')

    
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity;
            amount.innerText = data.amount;
            totalAmount.innerText = data.totalamount;
        }
    })

})


// code for decreasing the quantity

$('.minus-cart').click(function(){
    let id = $(this).attr("pid").toString();
    let eml = this.parentNode.children[2];
    let amount = document.querySelector('#amount');
    let totalAmount = document.querySelector('#totalamount')

    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success: function(data){
            eml.innerText = data.quantity;
            amount.innerText = data.amount;
            totalAmount.innerText = data.totalAmount;
        }

    })

})


// code for removing the producty from the cart
$('.remove-item').click(function(){
    let id = $(this).attr("pid").toString();
    let cart_items = document.querySelector('#cart-item');
    
    let elm = this;
    // let amount = document.querySelector('#amount');
    // let totalAmount = document.querySelector('#totalamount')

    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.total_amount;
            elm.parentNode.parentNode.parentNode.parentNode.remove()
        
   
        }

    })

})
