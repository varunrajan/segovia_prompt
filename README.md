# Segovia Deployment Manager Coding Exercise

## Conclusions and next steps

### Result

You can find the script and resulting transaction status message in [send_shillings.ipynb](https://github.com/varunrajan/segovia_prompt/blob/master/send_shillings.ipynb). For ease of access, I also included the script in [send_shillings.py](https://github.com/varunrajan/segovia_prompt/blob/master/send_shillings.py) as I noticed the `.ipynb` format takes some time and occasional refreshes to load properly in GitHub.

As you can see, I used the same function (`send_request_to_gateway`) to send the payment (to `/api/pay`) and subsequently check on the transaction's status (by sending the request to the `/api/transactionstatus` endpoint) so that I would receive a message about its status right away.

I tend to receive the following message, as the gateway has not yet attempted to process the payment:

```
{'transactions': [{'transactionId': 'f212f4c3-2efe-4abd-ab2f-ca174491e804',
   'transactionType': 'pay',
   'statusCode': 100,
   'statusDescription': 'The gateway has received the transaction.',
   'provider': 'autodetect',
   'finished': False,
   'statusType': 'pending'}],
 'finished': True}
```
 
To see the result after the transaction `statusType` is no longer `pending`, I've locally sent a request the `/api/transactionstatus` endpoint separately a few moments after sending the request to `/api/pay`, and received the following result:

```
{'transactions': [{'transactionId': 'f212f4c3-2efe-4abd-ab2f-ca174491e804',
   'statusCode': 406,
   'statusDescription': 'Cannot autodetect payment provider - recipient account ID 254999999999 is not a phone number with a valid country calling code',
   'finished': True,
   'statusType': 'failed',
   'transactionType': 'pay'}],
 'finished': True}
```

### Potential next steps

I understand that [Callbacks](https://docs.thesegovia.com/api-reference/#callbacks) are the preferred way to receive results. Were I building this script for a client or attempting to receive updates as the status of the transaction changed, I would attempt to use Callbacks as opposed to explicitly pinging the `/api/transactionstatus` endpoint.

Given that this particular transaction ultimately failed, I would also want to explore the underlying reasons why and hopefully resolve them.


## Context and instructions

We are excited that you are considering Segovia for your next role. As part of the interview process, we ask candidates to demonstrate their technical ability via a take-home exercise. Please take no more than 2 hours to finish this exercise.

Your task is to write a script that uses our public API to pay an amount to a recipient and then reports the status of that transaction immediately afterwards. For example, we'd like to send `1,200 Kenyan Shillings (KES)` to this phone number: `254999999999`.

Our public API is [here](https://docs.thesegovia.com/). You'll need a few pieces of basic information to get started:

- Public and private keys that you'll need are included in this package (and have already been registered on our servers)
- `key-id`: `er157YrM1WL`
- `client-id`: `homework-test`

We recommend looking at [Request Signatures](https://docs.thesegovia.com/signatures/) with some sample code to help you get started.

Please add suitable comments and explanation in your code as you see fit. If you don't finish or wish you could have done more at the end of the 2 hours, feel free to document what you would do next.

Happy coding!
