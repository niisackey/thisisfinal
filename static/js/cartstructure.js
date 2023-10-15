// cart
      const cart = {}; // Cart data structure (in-memory)

      function addToCart(productId, sizeId, quantityId) {
        const sizeSelect = document.getElementById(sizeId);
        const selectedSize = sizeSelect.options[sizeSelect.selectedIndex];
        const size = selectedSize.value;
        const price = parseFloat(selectedSize.getAttribute("data-price"));

        const quantityInput = document.getElementById(quantityId);
        const quantity = parseInt(quantityInput.value, 10);

        if (!cart[productId]) {
          cart[productId] = [];
        }

        const existingItem = cart[productId].find((item) => item.size === size);
        if (existingItem) {
          existingItem.quantity += quantity;
        } else {
          cart[productId].push({ size, price, quantity });
        }

        updateCartDisplay();
      }
      function removeFromCart(productId, size) {
        if (cart[productId]) {
          const itemIndex = cart[productId].findIndex(
            (item) => item.size === size
          );
          if (itemIndex !== -1) {
            const item = cart[productId][itemIndex];
            if (item.quantity === 1) {
              cart[productId].splice(itemIndex, 1);
            } else {
              item.quantity -= 1;
            }
          }
        }

        updateCartDisplay();
      }

      function updateCartDisplay() {
        const cartList = document.getElementById("cartItems");
        cartList.innerHTML = "";

        let totalAmount = 0;

        for (const productId in cart) {
          cart[productId].forEach((product) => {
            const listItem = document.createElement("li");
            listItem.textContent = `${
              product.size
            } - GHC ${product.price.toFixed(2)} x${product.quantity} = GHC ${(
              product.price * product.quantity
            ).toFixed(2)}`;

            const plusButton = document.createElement("button");
            plusButton.textContent = "+";
            plusButton.onclick = () => addToCart(productId, product.size);

            const minusButton = document.createElement("button");
            minusButton.textContent = "-";
            minusButton.onclick = () => removeFromCart(productId, product.size);

            listItem.appendChild(plusButton);
            listItem.appendChild(minusButton);
            cartList.appendChild(listItem);

            totalAmount += product.price * product.quantity;
          });
        }

        const cartSection = document.getElementById("cart");
        cartSection.style.display =
          Object.keys(cart).length > 0 ? "block" : "none";

        const cartItemCount = document.getElementById("cartItemCount");
        const totalItems = Object.values(cart).reduce(
          (total, items) =>
            total +
            items.reduce((itemTotal, item) => itemTotal + item.quantity, 0),
          0
        );
        cartItemCount.textContent = totalItems.toString();

        const cartTotal = document.getElementById("cartTotal");
        cartTotal.textContent = `Total: GHC ${totalAmount.toFixed(2)}`;
      }

      function toggleCart() {
        const cartSection = document.getElementById("cart");
        cartSection.style.display =
          cartSection.style.display === "none" ? "block" : "none";
      }

      async function checkout() {
        const customerNotes = document.getElementById("customerNotes").value;
        // cart['customerNotes'] = customerNotes
        console.log(cart);

        const combinedData = {
          data: cart,
          notes: customerNotes,
        };
        console.log(combinedData);

        try {
          console.log("customer notes", customerNotes);
          const response = await fetch("/submit_order", {
            method: "POST",
            body: JSON.stringify(combinedData),
            headers: {
              "Content-Type": "application/json",
            },
          });

          if (response.ok) {
            alert("Order placed successfully!. Thank you for believing in us");
            for (const productId in cart) {
              delete cart[productId];
            }
            updateCartDisplay();
          } else {
            alert("Order failed. Please try again.");
          }
        } catch (error) {
          console.error("Error:", error);
          alert(
            "An error occurred while placing the order. Please try again later."
          );
        }
      }
    