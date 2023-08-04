function change_price(x) {
    const id = x.dataset.id;
    console.log(id);
    const amount = x.dataset.amount;
    const serial = x.dataset.serial;
    const status = x.dataset.status;
    //const cart = JSON.parse(localStorage.getItem('cart'));
    console.log(status);
    document.querySelectorAll(`.price_btn_${id}`).forEach(function (button) {
        button.classList.remove("active");
    })
    x.classList.add("active");
    var element = document.querySelector(`.updated_price_${id}`);
    var second_element;
    if (status == "open") {
        second_element = document.querySelector(`.prev_price_${id}`);
    }





    //console.log(cart);

    //localStorage.setItem('cart', JSON.stringify(cart));
    //console.log(cart);

    fetch(`update_amount/${id}`, {
        method: 'GET'
    })
        .then((response) => response.json())
        .then(oud => {

            var num;
            var second_num;
            if (serial == 1) {
                num = oud.price_1;
                second_num = oud.prev_price_1;

            }
            else if (serial == 2) {
                num = oud.price_2;
                second_num = oud.prev_price_2;
            }
            else if (serial == 3) {
                num = oud.price_3;
                second_num = oud.prev_price_3;
            }
            else if (serial == 4) {
                num = oud.price_4;
                second_num = oud.prev_price_4;
            }
            element.innerHTML = num;
            if (status == "open") second_element.innerHTML = "Tk " + second_num;
            if (document.getElementById(`special_btn_${id}`)) {
                document.getElementById(`special_btn_${id}`).dataset.amount = amount;
            }
        });


}

window.addEventListener('scroll', function () {
    var main_header = document.querySelector('.main_header');
    var nav_bar = document.querySelector(".my_nav");
    var notice_board = document.querySelector(".noticeboard-div");
    if (window.scrollY > (main_header.offsetHeight / 2)) {
        main_header.classList.add("main_header_scrolled");
        document.querySelector('.navbar_brand').style.opacity = "0";
        var windowWidth = document.documentElement.clientWidth;
        if (windowWidth > 900) {
            nav_bar.classList.add("my_nav_scrolled");
        }

        if (notice_board) {
            notice_board.classList.add('noticeboard-div-scrolled');
        }



        document.querySelector('.ibnmain_name_li').style.display = "block";
        document.querySelector('.ibnmain-writeup').style.display = "block";
        document.querySelector('.ibnmain-img-mobile').style.display = "none";
    }
    else {
        main_header.classList.remove("main_header_scrolled");
        document.querySelector('.navbar_brand').style.opacity = "1";
        nav_bar.classList.remove("my_nav_scrolled");
        if (notice_board) {
            notice_board.classList.remove('noticeboard-div-scrolled');
        }

        document.querySelector('.ibnmain_name_li').style.display = "none";
        document.querySelector('.ibnmain-writeup').style.display = "none";
        document.querySelector('.ibnmain-img-mobile').style.display = "block";
    }


});






document.addEventListener('DOMContentLoaded', function () {
    /*
    let shah_img_1st = document.querySelector('.shah-1st-image');
    let story_of_shah = document.querySelector(".story_of_shahjahan");
    let posn = story_of_shah.offsetTop;


    let shah_img_2nd = document.querySelector('.shah-2nd-image');
    let shah_img_3rd = document.querySelector('.shah-3rd-image');
    let shah_img_4th = document.querySelector('.shah-4th-image');
    window.addEventListener('scroll', function () {

        if (window.pageYOffset >= (posn - 450)) {
            shah_img_1st.style.animationName = "topSlideIn";
        }
        if (window.pageYOffset >= (posn - 400)) {
            shah_img_2nd.style.animationName = "rightSlideIn";
        }
        if (window.pageYOffset >= (posn - 150)) {
            shah_img_3rd.style.animationName = "leftSlideIn";
        }
        if (window.pageYOffset >= (posn - 100)) {
            shah_img_4th.style.animationName = "bottomSlideIn";
        }

    });

    */

    if (localStorage.getItem('cart') == null) {
        var cart = {};
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    else {
        cart = JSON.parse(localStorage.getItem('cart'));
    }

    if (localStorage.getItem('cart_state') == null) {
        var cart_state = {};
        var state = 1;
        cart_state["cart"] = state;
        cart_state["delivery_charge"] = 70;
        cart_state["promo_discount"] = 0;
        cart_state["promo_name"] = "none";
        cart_state["sum"] = 0;
        cart_state["user_state"] = 1;
        localStorage.setItem('cart_state', JSON.stringify(cart_state));
    }
    else {
        cart_state = JSON.parse(localStorage.getItem('cart_state'));
    }

});

/*
setInterval(function(){
    document.querySelectorAll(".granite_slide").forEach(function(slide){
        slide.classList.remove("first_g");
    })
    console.log(second_counter);
    document.getElementById('radio_g_' + second_counter).checked = true;
    document.getElementById('slide_g_' + second_counter).classList.toggle("first_g");
    document.querySelectorAll(".manual-btn-g").forEach(function(btn){
        btn.style.backgroundColor = "rgba(255, 255, 255, 0.1)";
        btn.style.paddingLeft = "20px";
        btn.style.paddingRight = "20px";
    });
    document.querySelectorAll(".manual-btn-g").forEach(function(btn){
        if(second_counter == parseInt(btn.dataset.id)){
            btn.style.backgroundColor = "white";
            btn.style.paddingRight = "50px";
            btn.style.paddingLeft = "50px";
        }
    });
    
    second_counter++;
    if(second_counter > 3){
        second_counter = 1;
    }
}, 5000);

*/








if (localStorage.getItem('cart') == null) {
    var cart = {};
    localStorage.setItem('cart', JSON.stringify(cart));
}
else {
    cart = JSON.parse(localStorage.getItem('cart'));
}


if (localStorage.getItem('cart_state') == null) {
    var cart_state = {};
    var state = 1;
    cart_state["cart"] = state;
    cart_state["delivery_charge"] = 70;
    cart_state["promo_discount"] = 0;
    cart_state["promo_name"] = "none";
    cart_state["sum"] = 0;
    cart_state["user_state"] = 1;
    localStorage.setItem('cart_state', JSON.stringify(cart_state));
}
else {
    cart_state = JSON.parse(localStorage.getItem('cart'));
}





function add_cart_func(x) {

    let idstr = x.id.toString();
    let product_id = x.dataset.id;
    let name_of_product = x.dataset.name;
    let amount = x.dataset.amount;
    let amount_number = x.dataset.amountnumber;
    let category = x.dataset.category;
    let cart_state = JSON.parse(localStorage.getItem('cart_state'));
    let cart = JSON.parse(localStorage.getItem('cart'));
    const amount_arr = [];
    const price_arr = [];
    const prev_price_arr = [];
    let img_url = x.dataset.imgurl;

    const bruh_div = document.querySelector(".cart-product-div");




    for (var i = 1; i <= parseInt(amount_number); i++) {
        // there is a potential bug which might be needed to be addressed later......
        var a = document.getElementById(`hidden_inp_${i}_${idstr}`).value;
        var b = document.getElementById(`hidden_inp1_${i}_${idstr}`).value;
        var c = document.getElementById(`hidden_inp2_${i}_${idstr}`).value;
        amount_arr.push(parseFloat(a));
        price_arr.push(parseFloat(b));
        prev_price_arr.push(parseFloat(c));
    }

    let sum = cart_state["sum"];
    


    let j = 0;

    while (cart[idstr + "_" + j] != undefined) {
        j++;
    }
    idstr = idstr + "_" + j;




    if (cart[idstr] != undefined) {
        qty = cart[idstr][0] + 1;
        cart[idstr] = [qty, name_of_product, id, amount, amount_number, amount_arr, category, price_arr, prev_price_arr, img_url]
    }
    else {
        qty = 1;
        //name_of_product = x.dataset.name;
        id = product_id;

        cart[idstr] = [qty, name_of_product, id, amount, amount_number, amount_arr, category, price_arr, prev_price_arr, img_url];
    }

    let product_div = document.createElement("div");
    let product_div1 = document.createElement("div");
    let product_div2 = document.createElement("div");
    let product_div_main = document.createElement("div");
    let product_div3 = document.createElement("div");
    product_div_main.classList.add("separate-cart-outer-div");
    product_div.classList.add("separate-cart-inner-div");
    product_div1.classList.add("separate-cart-inner-div-img");
    product_div2.classList.add("separate-cart-inner-div-content");
    product_div3.classList.add("separate-cart-inner-div-price")

    let img = document.createElement("img");
    img.src = img_url;
    img.alt = "This image doesn't exist";
    product_div1.appendChild(img);
    let h1 = document.createElement("h1");
    h1.innerHTML = name_of_product;

    product_div_main.id = `this-cart-prod-div-${idstr}`;
    

    product_div2.appendChild(h1);

    let p1 = document.createElement("p");
    let p2 = document.createElement('p');
    let p3 = document.createElement("p");
    let p4 = document.createElement("p");
    let p5 = document.createElement("a");

    

    p1.innerHTML = "Qty: x" + qty;
    p2.innerHTML = "Amount: " + amount + " gm";
    p1.id = `cart-prod-div-quantity-${idstr}`;
    p2.id = `cart-prod-div-amount-${idstr}`;


    var serial = 0;

    for (var i = 0; i < amount_number; i++) {
        if (cart[idstr][5][i] === parseFloat(amount)) {
            serial = i;
        }
    }
    var total_price = qty * cart[idstr][7][serial];
    p3.innerHTML = "Price: " +cart[idstr][7][serial] + " BDT";
    product_div.dataset.price = total_price;
    p4.innerHTML = total_price + " BDT";
    p4.id = `cart-prod-div-total-price-${idstr}`;
    p5.innerHTML = "Remove";
    p5.classList.add("remove-from-cart-btn");
    p5.onclick = function() {
        remove_from_cart(idstr); // Pass your item ID or any relevant data as needed   
    };  

    sum += total_price;

    cart_state["sum"] = sum;
    p3.id = `cart-prod-div-price-${idstr}`;
    p3.dataset.value = total_price;
    product_div3.appendChild(p1);
    product_div3.appendChild(p4);
    product_div3.appendChild(p5);
    product_div2.appendChild(p2);
    product_div2.appendChild(p3);
    product_div.appendChild(product_div1);
    product_div.appendChild(product_div2);
    product_div_main.appendChild(product_div);
    product_div_main.appendChild(product_div3);

    if (Object.keys(cart).length === 1) {
        bruh_div.innerHTML = "";
        bruh_div.appendChild(product_div_main);
    }
    else {
        bruh_div.appendChild(product_div_main);
    }

    document.querySelector('.cart-subtotal-price-span').innerHTML = sum;
    localStorage.setItem('cart', JSON.stringify(cart));
    localStorage.setItem('cart_state', JSON.stringify(cart_state));
    console.log(cart);
    


    document.querySelectorAll("#nav_cart").forEach(function (div) { div.innerHTML = Object.keys(cart).length });
    //update_cart(cart, idstr);

    showAlert('Product Added', `${name_of_product} has been added to Your cart`, '#155724', '#d4edd9');
}

function remove_item(x) {
    let id = x.dataset.id;
    let product_div = document.getElementById(`this-cart-prod-div-${id}`);
    product_div.remove();
    let cart = JSON.parse(localStorage.getItem('cart'));
    let cart_state =JSON.parse(localStorage.getItem('cart_state'));
    let sum = cart_state["sum"];
    let price = product_div.dataset.price;
    sum -= price;
    document.querySelector('.cart-subtotal-price-span').innerHTML = sum;
    delete cart[id];
    cart_state["sum"] = sum;
    
    localStorage.setItem('cart', JSON.stringify(cart));
    localStorage.setItem('cart_state', JSON.stringify(cart_state));
    document.querySelectorAll("#nav_cart").forEach(function (div) { div.innerHTML = Object.keys(cart).length });
    if (Object.keys(cart).length === 0) {
        bruh_div.innerHTML = "You have not added any product to your cart. Thus it is empty.";
    }
    showAlert('Product Removed', `${oud_name} has been removed From your cart`, '#856305', '#fff2cd');
}



function remove_from_cart(item){
    console.log(item);
    console.log("Comes here");
    document.querySelector(`#this-cart-prod-div-${item}`).remove();
    let cart = JSON.parse(localStorage.getItem('cart'));
    let cart_state =JSON.parse(localStorage.getItem('cart_state'));
    let sum = cart_state["sum"];
    let price = cart[item][0] * cart[item][7][0];
    sum -= price;
    document.querySelector('.cart-subtotal-price-span').innerHTML = sum;
    showAlert('Product Removed', `${cart[item][1]} has been removed From your cart`, '#856305', '#fff2cd');
    delete cart[item];
    cart_state["sum"] = sum;
    console.log(cart);
    
    localStorage.setItem('cart', JSON.stringify(cart));
    localStorage.setItem('cart_state', JSON.stringify(cart_state));
    //document.querySelectorAll("#nav_cart").forEach(function (div) { div.innerHTML = Object.keys(cart).length });
    if (Object.keys(cart).length === 0) {
        bruh_div.innerHTML = "You have not added any product to your cart. Thus it is empty.";
    }

    document.querySelectorAll("#nav_cart").forEach(function (div) { div.innerHTML = Object.keys(cart).length });
    
}


function subtract_func(x) {
    id = x.dataset.id;
    cart = JSON.parse(localStorage.getItem('cart'));
    cart[id][0] = cart[id][0] - 1;
    cart[id][0] = Math.max(0, cart[id][0]);
    if (cart[id][0] == 0) {
        let oud_id = x.dataset.oud;
        let oud_name = x.dataset.name;
        let amount = x.dataset.amount;
        let amount_number = x.dataset.amountnumber;
        let category = x.dataset.category;
        let img_url = x.dataset.imgurl;
        let product_div = document.getElementById(`this-cart-prod-div-${id}`);
        const bruh_div = document.querySelector(".cart-product-div");
        product_div.remove();
        delete cart[id];
        document.getElementById(`div_${id}`).innerHTML = `<button class="btn btn-outline-primary cart cart-btn" id="${id}" data-id='${oud_id}' onclick="add_cart_func(this)" data-name='${oud_name}' data-amount="${amount}" 
                                                            data-amountnumber='${amount_number}' data-category='${category}' data-imgurl='${img_url}'><i class="bi bi-cart"></i> Add to Cart</button>`;
        console.log(cart);
        localStorage.setItem('cart', JSON.stringify(cart));
        document.querySelectorAll("#nav_cart").forEach(function (div) { div.innerHTML = Object.keys(cart).length });
        if (Object.keys(cart).length === 0) {
            bruh_div.innerHTML = "You have not added any product to your cart. Thus it is empty.";
        }
        showAlert('Product Removed', `${oud_name} has been removed From your cart`, '#856305', '#fff2cd');
    }
    else {
        document.getElementById(`val_${id}`).innerHTML = cart[id][0];
        const price_elem = document.getElementById(`cart-prod-div-price-${id}`);
        let val = price_elem.dataset.value;

        const qty_elem = document.getElementById(`cart-prod-div-quantity-${id}`);

        qty_elem.innerHTML = "Quantity: x" + cart[id][0];
        var i;
        for (i = 0; i < parseInt(cart[id][4]); i += 1) {
            if (parseFloat(cart[id][3]) === parseFloat(cart[id][5][i])) {
                break;
            }
        }


        let price = cart[id][7][i] * cart[id][0];

        price_elem.innerHTML = "Total Price: " + price + " BDT";
        price_elem.dataset.value = price;
        console.log(cart);

        localStorage.setItem('cart', JSON.stringify(cart));
    }
}

function add_func(x) {

    console.log("adds");
    cart = JSON.parse(localStorage.getItem('cart'));
    id = x.dataset.id;
    cart[id][0] = cart[id][0] + 1;
    document.getElementById(`val_${id}`).innerHTML = cart[id][0];

    const price_elem = document.getElementById(`cart-prod-div-price-${id}`);
    let val = price_elem.dataset.value;

    const qty_elem = document.getElementById(`cart-prod-div-quantity-${id}`);

    qty_elem.innerHTML = "Quantity: x" + cart[id][0];

    var i;
    for (i = 0; i < parseInt(cart[id][4]); i += 1) {
        if (parseFloat(cart[id][3]) === parseFloat(cart[id][5][i])) {
            break;
        }
    }



    let price = cart[id][7][i] * cart[id][0];
    price_elem.innerHTML = "Total Price: " + price + " BDT";
    price_elem.dataset.value = price;
    console.log(cart);
    localStorage.setItem('cart', JSON.stringify(cart));
}

function update_cart(cart, item) {
    const btn = document.getElementById(item);
    let id = btn.dataset.id;
    let name = btn.dataset.name;
    let amount = btn.dataset.amount;
    let amount_number = btn.dataset.amountnumber;
    let category = btn.dataset.category;
    let img_url = btn.dataset.imgurl;




    document.getElementById(`div_${item}`).innerHTML = `<button id='minus_${item}'
    class = 'btn btn-outline-primary cart' data-id='${item}' onclick='subtract_func(this)' data-oud='${id}' data-name='${name}' data-amount='${amount}' data-amountnumber='${amount_number}' data-category='${category}' data-imgurl='${img_url}'>-</button> <span id='val_${item}'>${cart[item][0]}
    </span> <button id='plus_${item}'class = 'btn btn-outline-primary cart' data-id='${item}' onclick='add_func(this)' data-oud='${id}' data-amount='${amount}' data-amountnumber='${amount_number}' data-imgurl='${img_url}'>+</button>`;


    document.querySelectorAll("#nav_cart").forEach(function (div) { div.innerHTML = Object.keys(cart).length });
}


function clearCart() {
    cart = localStorage.getItem('cart');
    cart = {};
    localStorage.removeItem('cart');
    const bruh_div = document.querySelector(".cart-product-div");
    bruh_div.innerHTML = "You have not added any product to your cart. Thus it is empty.";
    //localStorage.removeItem('cart');
    document.querySelectorAll("#nav_cart").forEach(function (div) { div.innerHTML = Object.keys(cart).length });
}


function show_menu() {
    let x = document.querySelector(".my_nav");
    let nice = document.querySelector(".menu_bar_x");

    nice.style.left = "93%";
    //nice.style.right = 0;
    x.style.left = 0;
}

function showAlert(heading, text, primary_color, secondary_color, confetti="") {
    let alert_div = document.querySelector('.alert-special-div');
    let alert_h1 = document.querySelector('.alert-heading');
    let alert_text = document.querySelector('.alert-text');
    alert_h1.innerHTML = heading;
    alert_text.innerHTML = text;
    alert_div.style.left = "50px";
    alert_div.style.color = primary_color;
    alert_div.style.backgroundColor = secondary_color;

    setTimeout(function () {
        alert_div.style.left = "-100%";
    }, 5000);

    if(confetti === "Done"){
        const jsConfetti = new JSConfetti();
        jsConfetti.addConfetti({
            confettiNumber: 1000,
            confettiColors: [
                '#cd0a54', '#0647ff', '#ff70ff', '#7885ff', '#fbb1bd', '#f9bec7',
            ],
        });
    }

}

function hide_menu() {
    let x = document.querySelector(".my_nav");
    x.style.left = "-100%";
    let nice = document.querySelector(".menu_bar_x");
    nice.style.left = "-100%";
}


function show_search_bar() {
    document.querySelectorAll(".nav-search-form").forEach(function (div) {
        div.style.display = "inline-block";
        //div.fadeToggle("slow");

    });

    document.querySelectorAll(".search-nav-writeup").forEach(function (div) {
        div.style.display = "none";
    });
    document.querySelectorAll(".search_icon").forEach(function (div) {
        div.style.display = "none";
    });

}

function hide_search(x) {
    document.querySelectorAll(".nav-search-form").forEach(function (div) {
        div.style.display = "none";
        //div.fadeToggle("slow");

    });

    document.querySelectorAll(".search-nav-writeup").forEach(function (div) {
        div.style.display = "inline-block";
    });

    document.querySelectorAll(".search_icon").forEach(function (div) {
        if (x == 'src-search-1') {
            div.style.display = "inline-block";
        }
        else {
            div.style.display = "inline-block";
        }
    });
}

function show_account_div() {
    const div = document.querySelector(".separate-account-div");
    div.style.right = "0";
    document.body.classList.toggle("overlay");
    div.style.opacity = "1";

}


function edit_in_profile() {
    document.querySelectorAll('.profile-page-inp').forEach(function (input) {
        input.disabled = false;
    });
    document.getElementById('profile-change-button').setAttribute("type", "submit");
    document.querySelectorAll('.profile-change-button-1').forEach(function (button) {
        button.style.display = "none";
    });

    document.querySelector('.profile-page-inp').focus;

}

function show_shipping_edit_div(x) {
    let id = x.dataset.id;
    const div = document.querySelector(`#i_${id}_edit_form`);
    div.style.display = "block";
    document.body.classList.toggle("overlay");
}

function hide_edit_shipping_div(x) {
    let id = x.dataset.id;
    const div = document.querySelector(`#i_${id}_edit_form`);
    div.style.display = "none";
    document.body.classList.toggle("overlay");
}

function show_shipping_div() {
    const div = document.querySelector("#new-shipping-form");
    div.style.display = "block";
    document.body.classList.toggle("overlay");
}

function hide_shipping_div() {
    const div = document.querySelector("#new-shipping-form");
    div.style.display = "none";
    document.body.classList.toggle("overlay");
}


function hide_account_div() {
    const div = document.querySelector(".separate-account-div");
    div.style.right = "-100%";
    document.body.classList.remove("overlay");
    div.style.opacity = "1";

}

function show_cart_div() {
    const div = document.querySelector(".separate-cart-div");
    div.style.right = "0";
    document.body.classList.toggle("overlay");
    div.style.opacity = "1";
    const bruh_div = document.querySelector(".cart-product-div");

    if (Object.keys(cart).length == 0) {
        bruh_div.innerHTML = "You have not added any product to your cart. Thus it is empty."
    }
    else {
        /*
        for (var item in cart) {
            var qty = cart[item][0];
            var name = cart[item][1];
            var img_url = cart[item][9];
            var amount_number = cart[item][4];
            var amount = cart[item][3];
            let product_div = document.createElement("div");
            let product_div1 = document.createElement("div");
            let product_div2 = document.createElement("div");

            product_div.classList.add("separate-cart-inner-div");
            product_div1.classList.add("separate-cart-inner-div-img");
            product_div2.classList.add("separate-cart-inner-div-content");

            let img = document.createElement("img");
            img.src = img_url;
            img.alt = "This image doesn't exist";
            product_div1.appendChild(img);
            let h1 = document.createElement("h1");
            h1.innerHTML = name;

            product_div2.appendChild(h1);

            let p1 = document.createElement("p");
            let p2 = document.createElement('p');
            let p3 = document.createElement("p");

            p1.innerHTML = "Quantity: x" + qty;
            p2.innerHTML = "Amount: " + amount + " gm";

            var serial = 0;

            for (var i = 0; i < amount_number; i++) {
                if (cart[item][5][i] === parseFloat(amount)) {
                    serial = i;
                }
            }
            var total_price = qty * cart[item][7][serial];
            p3.innerHTML = "Total Price: " + total_price + " BDT";
            product_div2.appendChild(p1);
            product_div2.appendChild(p2);
            product_div2.appendChild(p3);
            product_div.appendChild(product_div1);
            product_div.appendChild(product_div2);
            bruh_div.appendChild(product_div);
            
        }
        */
    }
}

function hide_cart_div() {
    const div = document.querySelector(".separate-cart-div");
    div.style.right = "-100%";
    document.body.classList.remove("overlay");
    div.style.opacity = "1";
}


function show_admin_page_notice() {
    show_admin_page_products()
    const all_product_div = document.querySelector(".admin-page-edit-product");
    const category_div = document.querySelector(".admin-page-categories");
    const promo_div = document.querySelector(".admin-page-promos");
    const quantity_div = document.querySelector(".admin-page-quantity_management");
    const notice_div = document.querySelector(".admin-page-notice");


    all_product_div.style.display = "none";
    category_div.style.display = "none";
    promo_div.style.display = "none";
    quantity_div.style.display = "none";
    notice_div.style.display = "block";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Notice";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}



function show_admin_page_products() {

    const dashboard = document.querySelector(".admin-page-dashboard");
    const product_div = document.querySelector(".admin-page-products");
    const user_div = document.querySelector(".admin-page-users");
    const order_div = document.querySelector(".admin_page_orders");
    const content_div = document.querySelector(".admin-page-content-management");
    const contact_div = document.querySelector(".admin-page-contact-us");

    dashboard.style.display = "none";
    product_div.style.display = "block";
    user_div.style.display = "none";
    order_div.style.display = "none";
    content_div.style.display = "none";
    contact_div.style.display = "none";
}


function show_admin_page_users() {
    const dashboard = document.querySelector(".admin-page-dashboard");
    const product_div = document.querySelector(".admin-page-products");
    const user_div = document.querySelector(".admin-page-users");
    const order_div = document.querySelector(".admin_page_orders");
    const content_div = document.querySelector(".admin-page-content-management");
    const contact_div = document.querySelector(".admin-page-contact-us");

    dashboard.style.display = "none";
    product_div.style.display = "none";
    user_div.style.display = "block";
    order_div.style.display = "none";
    content_div.style.display = "none";
    contact_div.style.display = "none";
}

function show_admin_page_orders() {
    const dashboard = document.querySelector(".admin-page-dashboard");
    const product_div = document.querySelector(".admin-page-products");
    const user_div = document.querySelector(".admin-page-users");
    const order_div = document.querySelector(".admin_page_orders");
    const content_div = document.querySelector(".admin-page-content-management");
    const contact_div = document.querySelector(".admin-page-contact-us");

    dashboard.style.display = "none";
    product_div.style.display = "none";
    user_div.style.display = "none";
    order_div.style.display = "block";
    content_div.style.display = "none";
    contact_div.style.display = "none";
}

function show_admin_page_contents() {
    const dashboard = document.querySelector(".admin-page-dashboard");
    const product_div = document.querySelector(".admin-page-products");
    const user_div = document.querySelector(".admin-page-users");
    const order_div = document.querySelector(".admin_page_orders");
    const content_div = document.querySelector(".admin-page-content-management");
    const contact_div = document.querySelector(".admin-page-contact-us");

    dashboard.style.display = "none";
    product_div.style.display = "none";
    user_div.style.display = "none";
    order_div.style.display = "none";
    content_div.style.display = "block";
    contact_div.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Contents";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));


}

function show_admin_page_dashboard() {
    const dashboard = document.querySelector(".admin-page-dashboard");
    const product_div = document.querySelector(".admin-page-products");
    const user_div = document.querySelector(".admin-page-users");
    const order_div = document.querySelector(".admin_page_orders");
    const content_div = document.querySelector(".admin-page-content-management");
    const contact_div = document.querySelector(".admin-page-contact-us");

    dashboard.style.display = "block";
    product_div.style.display = "none";
    user_div.style.display = "none";
    order_div.style.display = "none";
    content_div.style.display = "none";
    contact_div.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "dashboard";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}


function show_admin_page_contact_us() {
    const dashboard = document.querySelector(".admin-page-dashboard");
    const product_div = document.querySelector(".admin-page-products");
    const user_div = document.querySelector(".admin-page-users");
    const order_div = document.querySelector(".admin_page_orders");
    const content_div = document.querySelector(".admin-page-content-management");
    const contact_div = document.querySelector(".admin-page-contact-us");

    dashboard.style.display = "none";
    product_div.style.display = "none";
    user_div.style.display = "none";
    order_div.style.display = "none";
    content_div.style.display = "none";
    contact_div.style.display = "block";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "contact_us";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}


function show_admin_page_allProducts() {
    show_admin_page_products()
    const all_product_div = document.querySelector(".admin-page-edit-product");
    const category_div = document.querySelector(".admin-page-categories");
    const promo_div = document.querySelector(".admin-page-promos");
    const quantity_div = document.querySelector(".admin-page-quantity_management");


    all_product_div.style.display = "block";
    category_div.style.display = "none";
    promo_div.style.display = "none";
    quantity_div.style.display = "none";
    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "allProducts";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}


function show_admin_page_category() {
    show_admin_page_products()
    const all_product_div = document.querySelector(".admin-page-edit-product");
    const category_div = document.querySelector(".admin-page-categories");
    const promo_div = document.querySelector(".admin-page-promos");
    const quantity_div = document.querySelector(".admin-page-quantity_management");
    const notice_div = document.querySelector(".admin-page-notice");


    all_product_div.style.display = "none";
    category_div.style.display = "block";
    promo_div.style.display = "none";
    quantity_div.style.display = "none";
    notice_div.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Categories";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}

function show_admin_page_promos() {
    show_admin_page_products()
    const all_product_div = document.querySelector(".admin-page-edit-product");
    const category_div = document.querySelector(".admin-page-categories");
    const promo_div = document.querySelector(".admin-page-promos");
    const quantity_div = document.querySelector(".admin-page-quantity_management");
    const notice_div = document.querySelector(".admin-page-notice");


    all_product_div.style.display = "none";
    category_div.style.display = "none";
    promo_div.style.display = "block";
    quantity_div.style.display = "none";
    notice_div.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Promos";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}

function show_admin_page_quantity() {
    show_admin_page_products()
    const all_product_div = document.querySelector(".admin-page-edit-product");
    const category_div = document.querySelector(".admin-page-categories");
    const promo_div = document.querySelector(".admin-page-promos");
    const quantity_div = document.querySelector(".admin-page-quantity_management");
    const notice_div = document.querySelector(".admin-page-notice");


    all_product_div.style.display = "none";
    category_div.style.display = "none";
    promo_div.style.display = "none";
    quantity_div.style.display = "block";
    notice_div.style.display = "none";
    let admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Quantity";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}


function show_user_page_profile(x) {
    let what = x.dataset.what;
    document.querySelectorAll('.user-div').forEach(function (div) {
        div.style.display = "none";
    });

    const div1 = document.querySelector(`.user-page-${what}`);
    div1.style.display = "block";

    let cart_state = JSON.parse(localStorage.getItem('cart_state'));
    if (what === "profile") {
        cart_state["user_state"] = 1;
    }
    else if (what === "orders") {
        cart_state["user_state"] = 2;
    }
    else if (what === "shipping-address") {
        cart_state["user_state"] = 3;
    }
    else if (what === "wishlist") {
        cart_state["user_state"] = 4;
    }
}

function show_user_page_div(what) {

    document.querySelectorAll('.user-div').forEach(function (div) {
        div.style.display = "none";
    });

    const div1 = document.querySelector(`.user-page-${what}`);
    div1.style.display = "flex";
}



function proceedToCheckout() {

    let cart_state = JSON.parse(localStorage.getItem('cart_state'));
    const btn1 = document.getElementById("state-1");
    const btn2 = document.getElementById("state-2");
    const btn3 = document.getElementById("state-3");
    const btn4 = document.getElementById("state-2-back");
    const btn5 = document.getElementById("state-3-back");

    document.querySelectorAll(".state-button").forEach(function (button) {
        button.classList.remove('state-next');
    });
    btn1.classList.add('state-next');
    btn2.classList.add('state-next');
    btn4.style.display = "block";
    btn5.style.display = "none";
    hr1.classList.add('dark-hr');
    hr2.classList.remove('dark-hr');

    document.querySelectorAll('.phase-1').forEach(function (div) {
        div.style.display = "none";
    });

    document.querySelectorAll('.phase-3').forEach(function (div) {
        div.style.display = "none";
    });

    document.querySelectorAll('.phase-2').forEach(function (div) {
        div.style.display = "block";
    });


    let cart_div = document.querySelector(".cart-main-div");
    cart_div.classList.remove("cart-main-div");
    cart_div.classList.add("cart-main-div-phase-2");
    console.log("success?");
    document.querySelector(".checkout-form-div").style.display = "flex";
    // document.querySelectorAll(".cart-internal-div2").forEach((div) => {
    //     div.style.display = "none";
    // })

    // document.querySelectorAll(".cart-page-table").forEach((div) => {
    //     div.style.display = "block";
    // })
    const cart = JSON.parse(localStorage.getItem('cart'));
    for (let item in cart) {
        let minus_btn = document.querySelector(`#minus_${item}`);
        let plus_btn = document.querySelector(`#plus_${item}`);
        let amount_selection = document.querySelector(`#amount_selection_${item}`);
        let amount_selection_p = document.querySelector(`#amount_selection_p_${item}`);
        let img_div = document.getElementById(`main-img-div-${item}`);
        let content_div = document.getElementById(`main-content-div-${item}`);
        let main_div = document.getElementById(item);
        //var qty_div = document.getElementById(`div_${item}`);
        //let price_div = document.getElementById(`price_${item}`);

        //qty_div.classList.remove('display_flex');

        img_div.classList.remove('main-cart-page-div1');
        img_div.classList.add('main-cart-page-div1-phase-2');

        content_div.classList.remove('main-cart-page-div2');
        content_div.classList.add('main-cart-page-div2-phase-2');

        main_div.classList.remove('main-cart-page-div');
        main_div.classList.add('main-cart-page-div-phase-2');
        minus_btn.disabled = true;
        plus_btn.disabled = true;
        //main_div.style.flexDirection = "column";
        amount_selection.style.display = "none";
        //qty_div.innerHTML = `<p>Qty: x${cart[item][0]}</p>`;
        //price_div.innerHTML = `<p>Price: BDT${price_div.dataset.value} </p>`;

        amount_selection_p.innerHTML = `<p>Amount : ` + cart[item][3] + " gm</p>";
        console.log(cart[item][3]);
        document.querySelector(`.button-phase-1`).style.display = "none";
    }
    cart_state["cart"] = 2;
    localStorage.setItem('cart_state', JSON.stringify(cart_state));
}


function checkAllInput() {
    var allFilled = true;
    document.querySelectorAll('.based_inp').forEach(function (input) {
        if (input.value === '') {
            allFilled = false;
            showPopover(input);

        }
    });




    if (allFilled) {
        proceedToPayment();
    }
}

function showPopover(input) {
    console.log("get called");
    // Create a popover element
    var popover = document.createElement('div');
    popover.className = 'popover_nice';
    popover.textContent = 'Please fill in this field.';

    // Position the popover next to the input field



    // Add the popover to the document
    console.log(input.name);
    const elem = document.querySelector(`#inp_div_${input.name}`);

    elem.append(popover);

    console.log(elem);
    input.classList.add('error-inp');

    input.focus();

    if (input.value.trim() === '') {
        window.scrollTo({
            top: elem.offsetTop - 100, // Scroll to the empty input
            behavior: 'smooth',
        });
    }


    // Remove the popover after 3 seconds
    setTimeout(function () {
        popover.remove();
        input.classList.remove('error-inp');
    }, 4000);
}

function proceedToPayment() {
    let cart_state = JSON.parse(localStorage.getItem('cart_state'));
    document.querySelectorAll('.phase-1').forEach(function (div) {
        div.style.display = "none";
    });

    const btn1 = document.getElementById("state-1");
    const btn2 = document.getElementById("state-2");
    const btn3 = document.getElementById("state-3");
    const btn4 = document.getElementById("state-2-back");
    const btn5 = document.getElementById("state-3-back");

    document.querySelectorAll(".state-button").forEach(function (button) {
        button.classList.remove('state-next');
    });
    btn1.classList.add('state-next');
    btn2.classList.add('state-next');
    btn3.classList.add('state-next');
    btn4.style.display = "block";
    btn5.style.display = "none";
    hr1.classList.add('dark-hr');
    hr2.classList.remove('dark-hr');



    document.querySelectorAll('.phase-2').forEach(function (div) {
        div.style.display = "none";
    });
    document.querySelectorAll('.phase-3').forEach(function (div) {
        div.style.display = "block";
    });
    document.querySelector('.cart_list').style.display = "none";
    cart_state['cart'] = 3;
    console.log("this works");
    document.querySelector('.payment-selection-div').style.display = "flex";
    localStorage.setItem('cart_state', JSON.stringify(cart_state));

}

function changePaymentSelection(x) {
    var type = x.dataset.type;
    if (type == 'online') {
        let payment_method = document.querySelector('#payment_method');
        payment_method.value = "online";
    }
    let div1 = document.querySelector('.payment-type-cash');
    let div2 = document.querySelector('.payment-type-online');
    let div3 = document.querySelector('.selected-p')
    let div4 = document.createElement("p");
    let inp = document.getElementById("payment_method");
    div4.classList.add("selected-p");
    div4.innerHTML = "Selected";

    div1.classList.toggle('selected');
    div2.classList.toggle('selected');
    div3.remove();


    if (type === 'cash') {
        div1.append(div4);
        inp.value = "Cash";
    }
    else {
        div2.append(div4);
        inp.value = "Online";
    }
}

function initial_cart_state() {
    let cart_state = JSON.parse(localStorage.getItem('cart_state'));
    const btn1 = document.getElementById("state-1");
    const btn2 = document.getElementById("state-2");
    const btn3 = document.getElementById("state-3");
    const btn4 = document.getElementById("state-2-back");
    const btn5 = document.getElementById("state-3-back");
    const hr1 = document.getElementById("state-hr-1");
    const hr2 = document.getElementById("state-hr-2");

    
    btn2.classList.remove('state-next');
    btn3.classList.remove('state-next');
    btn1.classList.add('state-next');
    btn4.style.display = "none";
    btn5.style.display = "none";
    hr1.classList.remove('dark-hr');
    hr2.classList.remove('dark-hr');


    if (cart_state["cart"] != 1) {
        let cart_div = document.querySelector(".cart-main-div-phase-2");
        cart_div.classList.add("cart-main-div");
        cart_div.classList.remove("cart-main-div-phase-2");
    }
    document.querySelectorAll('.phase-3').forEach(function (div) {
        div.style.display = "none";
    });

    document.querySelectorAll('.phase-2').forEach(function (div) {
        div.style.display = "none";
    });

    document.querySelectorAll('.phase-1').forEach(function (div) {
        div.style.display = "block";
    });

    // if(window.innerWidth > 762){
    //     document.querySelectorAll(".cart-internal-div2").forEach((div) => {
    //         div.style.display = "block";
    //     })
    
    //     document.querySelectorAll(".cart-page-table").forEach((div) => {
    //         div.style.display = "none";
    //     })

    //     console.log("this works");
    // }
    

    const cart = JSON.parse(localStorage.getItem('cart'));
    for (var item in cart) {
        let name = cart[item][1];
        let id = cart[item][2];
        let qty = cart[item][0];
        let amount = cart[item][3];
        let amount_number = cart[item][4];
        let img_url = cart[item][9];
        var amount_selection = document.querySelector(`#amount_selection_${item}`);
        var amount_selection_p = document.querySelector(`#amount_selection_p_${item}`);
        var img_div = document.getElementById(`main-img-div-${item}`);
        var content_div = document.getElementById(`main-content-div-${item}`);
        let minus_btn = document.querySelector(`#minus_${item}`);
        let plus_btn = document.querySelector(`#plus_${item}`);
        var main_div = document.getElementById(item);
        //var qty_div = document.getElementById(`div_${item}`);
        //var price_div = document.getElementById(`price_${item}`);

        //qty_div.classList.add('display_flex');

        minus_btn.disabled = false;
        plus_btn.disabled = false;

        img_div.classList.add('main-cart-page-div1');
        img_div.classList.remove('main-cart-page-div1-phase-2');

        content_div.classList.add('main-cart-page-div2');
        content_div.classList.remove('main-cart-page-div2-phase-2');

        main_div.classList.add('main-cart-page-div');
        main_div.classList.remove('main-cart-page-div-phase-2');

        amount_selection.style.display = "flex";
        var windowWidth = document.documentElement.clientWidth;
        if (windowWidth > 762) {
            //main_div.style.flexDirection = "row";
        }

        //qty_div.innerHTML = `<p class='quantity-writing'>Quantity: </p><button id='minus_${item}'
                                    //class = 'btn btn-outline-primary cart' data-id='${item}' onclick='subtract_func(this)' data-oud='${id}' data-name='${name}' data-amount='${amount}'   data-amountnumber='${amount_number}' data-imgurl='${img_url}'>-</button> <span id='val_${item}'>${cart[item][0]}
                                    //</span> <button id='plus_${item}'class = 'btn btn-outline-primary cart' data-id='${item}' onclick='add_func(this)' data-oud='${id}' data-amountnumber='${amount_number}'>+</button>`;


        //price_div.innerHTML = `<p>Price: BDT ${price_div.dataset.value} </p>`

        amount_selection_p.innerHTML = `Amount : `;
        console.log(cart[item][3]);
    }



    document.querySelector(`.button-phase-2`).style.display = "none";
    document.querySelector(".checkout-form-div").style.display = "none";
    document.querySelector('.cart_list').style.display = "flex";
    cart_state["cart"] = 1;
    localStorage.setItem('cart_state', JSON.stringify(cart_state));

}

function show_delete_box(x) {
    const id = x.dataset.id;
    const element = document.getElementById(`delete_box_${id}`);
    element.style.display = "flex";
}


function hide_delete_box(x) {
    const id = x.dataset.id;
    const element = document.getElementById(`delete_box_${id}`);
    element.style.display = "none";
}

function edit_category(x, name) {
    var id = x.dataset.id;
    const first_edit = document.querySelector(`#${name}_edit_1_${id}`);
    console.log(first_edit);
    first_edit.classList.toggle("not_visible");
    const second_edit = document.querySelector(`#${name}_edit_2_${id}`);
    console.log(second_edit);
    second_edit.classList.toggle("not_visible");
    document.querySelectorAll(`.${name}_name_${id}`).forEach(function (nice) {
        nice.classList.toggle("not_visible");
    });
    const category_div = document.querySelector(`#${name}_div_${id}`);
    category_div.classList.toggle("not_visible");
}



function edit_category_nice(x, name) {
    var id = x.dataset.id;
    var second = null;
    const inp_val = document.querySelector(`#${name}_input_${id}`);
    if (name === "promo") {
        const inp_val_2 = document.querySelector(`#${name}_inp_disc_${id}`);
        second = inp_val_2.value;
    }

    fetch(`edit/${name}/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            val: inp_val.value,
            val1: second,
        })
    })
        .then((response) => response.json())
        .then(info => {
            if (name === "category") {
                inp_val.value = info.name;
                const text = document.querySelector(`#${name}_p_${id}`);
                text.innerHTML = info.name;
            }
            if (name === "quantity") {
                inp_val.value = info.amount;
                const text = document.querySelector(`#${name}_p_${id}`);
                text.innerHTML = parseFloat(info.amount).toFixed(2) + " gm";
            }

            if (name === "promo") {
                inp_val.value = info.name;
                const text = document.querySelector(`#${name}_p_${id}`);
                text.innerHTML = info.name;
                document.querySelector(`#${name}_inp_disc_${id}`).value = info.discount_amount;
                const text1 = document.querySelector(`#promo_disc_${name}`);


            }

            edit_category(x, name);

        })

}


function show_admin_page_new_orders() {
    show_admin_page_orders();
    const div1 = document.querySelector(".admin-page-pending-orders");
    const div2 = document.querySelector(".admin-page-delivered-orders");
    const div3 = document.querySelector(".admin-page-cancelled-orders");

    div1.style.display = "block";
    div2.style.display = "none";
    div3.style.display = "none";
    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "New Orders";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}

function show_admin_page_delivered_orders() {
    show_admin_page_orders();
    const div1 = document.querySelector(".admin-page-pending-orders");
    const div2 = document.querySelector(".admin-page-delivered-orders");
    const div3 = document.querySelector(".admin-page-cancelled-orders");

    div1.style.display = "none";
    div2.style.display = "block";
    div3.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Delivered Orders";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}

function show_admin_page_cancel_orders() {
    show_admin_page_orders();
    const div1 = document.querySelector(".admin-page-pending-orders");
    const div2 = document.querySelector(".admin-page-delivered-orders");
    const div3 = document.querySelector(".admin-page-cancelled-orders");

    div1.style.display = "none";
    div2.style.display = "none";
    div3.style.display = "block";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Cancelled Orders";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}


function show_admin_page_admin() {
    show_admin_page_users();

    const div1 = document.querySelector(".admin-page-admins");
    const div2 = document.querySelector(".admin-page-moderators");
    const div3 = document.querySelector(".admin-page-all_users");
    const div4 = document.querySelector(".admin-page-view-reviews");

    div1.style.display = "block";
    div2.style.display = "none";
    div3.style.display = "none";
    div4.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Admin";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}

function show_category_delete_box(x, name) {
    var category_id = x.dataset.id;

    var div = document.querySelector(`#${name}_delete_${category_id}`);
    div.style.display = "flex";
}

function hide_category_delete_box(x, name) {
    var category_id = x.dataset.id;
    var div = document.querySelector(`#${name}_delete_${category_id}`);
    div.style.display = "none";
}


function show_admin_page_moderator() {
    show_admin_page_users();

    const div1 = document.querySelector(".admin-page-admins");
    const div2 = document.querySelector(".admin-page-moderators");
    const div3 = document.querySelector(".admin-page-all_users");
    const div4 = document.querySelector(".admin-page-view-reviews");

    div1.style.display = "none";
    div2.style.display = "block";
    div3.style.display = "none";
    div4.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Moderator";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}



function show_admin_page_user() {
    show_admin_page_users();

    const div1 = document.querySelector(".admin-page-admins");
    const div2 = document.querySelector(".admin-page-moderators");
    const div3 = document.querySelector(".admin-page-all_users");
    const div4 = document.querySelector(".admin-page-view-reviews");

    div1.style.display = "none";
    div2.style.display = "none";
    div3.style.display = "block";
    div4.style.display = "none";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "User";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));
}




function show_admin_page_reviews() {

    show_admin_page_users();

    const div1 = document.querySelector(".admin-page-admins");
    const div2 = document.querySelector(".admin-page-moderators");
    const div3 = document.querySelector(".admin-page-all_users");
    const div4 = document.querySelector(".admin-page-view-reviews");

    div1.style.display = "none";
    div2.style.display = "none";
    div3.style.display = "none";
    div4.style.display = "block";

    var admin_state = JSON.parse(localStorage.getItem('admin_state'));
    admin_state["admin"] = "Reviews";
    localStorage.setItem('admin_state', JSON.stringify(admin_state));

}

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}


function change_tracker_status(x, id) {
    let value = x.dataset.value;
    fetch(`/show_order/${id}/tracker/${value}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then((response) => response.json())
        .then(info => {
            for (var i = 0; i <= 3; i++) {
                document.querySelector(`#icon-${i}`).style.color = "rgba(128, 128, 128, 0.344)";
            }
            for (var i = 0; i <= parseInt(info.value); i++) {
                document.querySelector(`#icon-${i}`).style.color = "#bbffbb";
            }

            document.querySelector(`.progress-bar`).style.width = `${info.progress}%`;
        });

    //location.reload();
}


function change_admin_user_status(x, id){
    const admin_select = document.querySelector(`select[name='${x}-user-status-${id}']`);
    const ask_btn = document.querySelector(`.${x}-ask-btn-${id}`);
    ask_btn.style.display = "none";
    const confirm_btn = document.querySelector(`.${x}-confirm-btn-${id}`);
    confirm_btn.style.display = "block";
    admin_select.disabled = false;

}


function change_user_status(x, id){
    const admin_select = document.querySelector(`select[name='${x}-user-status-${id}`);
    const value = admin_select.value;
    const ask_btn = document.querySelector(`.${x}-ask-btn-${id}`);
    ask_btn.style.display = "block";
    const confirm_btn = document.querySelector(`.${x}-confirm-btn-${id}`);
    confirm_btn.style.display = "none";
    admin_select.disabled = true;

    fetch(`change_user_status/${id}/${value}`,{
        method: 'PUT',
    })
    .then((response) => response.json())
    .then(status =>{
        if(status.status == "passed"){
            showAlert('User Status Changed', `${status.user_name} is now a/an ${status.what}`, '#155724', '#d4edd9');
        }
        else{
            showAlert('Could Not Change Status', `${status.user_name}'s status isn't changed`, '#155724', '#d4edd9');
        }
    });

}

