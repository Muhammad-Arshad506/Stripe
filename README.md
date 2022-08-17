
# User Flow
After the user clicks the purchase button we need to do the following:

## step 1: Get Publishable Key

-Send an XHR request from the client to the server requesting the publishable key
-Respond with the key
-Use the key to create a new instance of Stripe.js


## step 2: Create Checkout Session

-Send another XHR request to the server requesting a new Checkout Session ID
-Generate a new Checkout Session and send back the ID
-Redirect to the checkout page for the user to finish their purchase

## step 3: Redirect the User Appropriately

-Redirect to a success page after a successful payment
-Redirect to a cancellation page after a cancelled payment

## step 4 :Confirm Payment with Stripe Webhooks

-Set up the webhook endpoint
-Test the endpoint using the Stripe CLI
-Register the endpoint with Stripe
