# grubhub

A quick wrapper around GrubHub's API, to fetch account and order information.

## Installation

This library is available on PyPI:

```python
pipenv install grubhub
```

## Example

```python
import grubhub
ghc = grubhub.GrubHubClient()
ghc.login(username="<username>", password="<password>")
orders = ghc.order_history()
```

and a sample order receipt:

```json
{
  "id": "a86651e0-59fa-11ec-81b3-cf196f90eedb",
  "group_id": "a86651e1-59fa-11ec-81b3-cf196f90eedb",
  "diner_info": {
    "id": "91d81980-6bda-11f6-b5e5-7930b4d5f97f",
    "name": "Jérémie Lumbroso",
    "email": "<username>",
    "phone": "<phone>"
  },
  "brand": "GRUBHUB",
  "when_for": "2021-12-10T19:10:24.663Z",
  "start_time": "2021-12-10T18:54:52.414Z",
  "time_placed": "2021-12-10T18:55:24.656Z",
  "currency": "USD",
  "fulfillment_info": {
    "type": "PICKUP",
    "pickup_info": {
      "name": "Jérémie Lumbroso",
      "phone": "<phone>",
      "email": "<username>",
      "green_indicated": false,
      "time_zone": {
        "id": "America/New_York",
        "name": "Eastern Standard Time",
        "raw_offset": -18000000
      },
      "handoff_options": []
    }
  },
  "charges": {
    "lines": {
      "diner_total": 555,
      "line_items": [
        {
          "id": "5413206376",
          "line_uuid": "qJx9ElnqEeygJwm_AhVS7g",
          "menu_item_id": "5413206376",
          "name": "House Brew Tea (Hot)",
          "price": 0,
          "quantity": 1,
          "adjustment_type": "NONE",
          "tags": [],
          "diner_total": 555,
          "options": [
            {
              "price": 555,
              "name": "L",
              "id": "5412398070",
              "quantity": 1,
              "option_tags": [],
              "child_options": []
            },
            {
              "price": 0,
              "name": "Oolong",
              "id": "5263934535",
              "quantity": 1,
              "option_tags": [],
              "child_options": []
            },
            {
              "price": 0,
              "name": "Extra Strong ",
              "id": "5413206372",
              "quantity": 1,
              "option_tags": [],
              "child_options": []
            }
          ],
          "special_instructions": "Please add VEGAN oat milk, thank you",
          "restaurant": {
            "id": "2421174",
            "name": "Ficus",
            "img_url": "https://res.cloudinary.com/grubhub/image/upload/rog5swk6meaw5rpllmkb.png",
            "media_image": {
              "base_url": "https://media-cdn.grubhub.com/image/upload/",
              "public_id": "rog5swk6meaw5rpllmkb",
              "format": "png",
              "tag": "logo"
            },
            "contact_free_required": false,
            "managed_delivery": false,
            "restaurant_tags": ["SUBSCRIPTION_ELIGIBLE_FOR_STANDARD_ORDER"]
          },
          "packaging_options": []
        }
      ]
    },
    "coupons": [],
    "diner_subtotal": 555,
    "non_itemized_adjustments": [],
    "fees": { "total": 0, "delivery": 0, "service": 0, "fee_items": [] },
    "donations": { "total": 0 },
    "taxes": { "total": 37, "sales": 37, "delivery": 0 },
    "tip": { "type": "INCLUDE_IN_BILL", "amount": 0, "tip_adjustments": [] },
    "diner_grand_total": 592
  },
  "payments": {
    "total": 592,
    "payments": [
      {
        "id": "s0TLyDvtRBqOzUl9xBavyz",
        "type": "APPLE_PAY",
        "amount": 592,
        "payment_uuid": "TlgrcApxNKeDMtjROzU7jQ",
        "metadata": {
          "credit_card_type": "Apple Pay - MasterCard",
          "payment_processor": "braintree",
          "expiration_date": "10/2024",
          "cc_last_four": "xxxx"
        },
        "amount_events": [
          {
            "amount_event_id": "QtrYvEu6P-iaZqvZRVP92A",
            "amount": 592,
            "updated_at": "2021-12-10T18:55:24.620Z"
          }
        ]
      }
    ]
  },
  "restaurants": [
    {
      "id": "2421174",
      "name": "Ficus",
      "img_url": "https://res.cloudinary.com/grubhub/image/upload/rog5swk6meaw5rpllmkb.png",
      "media_image": {
        "base_url": "https://media-cdn.grubhub.com/image/upload/",
        "public_id": "rog5swk6meaw5rpllmkb",
        "format": "png",
        "tag": "logo"
      },
      "contact_free_required": false,
      "managed_delivery": false,
      "restaurant_tags": ["SUBSCRIPTION_ELIGIBLE_FOR_STANDARD_ORDER"]
    }
  ],
  "reviews": [],
  "state": "COMPLETED",
  "order_number": "054217315097086",
  "order_tracking": { "enabled": false },
  "disallow_reorder": false,
  "was_preorder": false,
  "local_when_for": "14:10:24",
  "system_of_record": "bullrat",
  "order_status": "CONFIRMED",
  "expensing_details": {
    "expensing_allowed": true,
    "expense_at": "2021-12-11T19:10:24.663Z"
  },
  "adjustments": {
    "history": [
      {
        "order_request_uuid": "KGc4uMOvNgmOPQH_3jZtcQ",
        "ordering": 0,
        "timestamp": "2021-12-10T18:55:24.656Z",
        "payments": [{ "key": "TlgrcApxNKeDMtjROwU7jQ", "value": 592 }],
        "totals": [
          { "key": "TAXES_TOTAL", "value": 37 },
          { "key": "DMP_GRUBHUB_MARGIN_TAX_TOTAL", "value": 0 },
          { "key": "TAXABLE_TOTAL", "value": 555 },
          { "key": "MERCHANT_GRAND_TOTAL", "value": 592 },
          { "key": "GRAND_TOTAL", "value": 592 },
          { "key": "DINER_SUB_TOTAL", "value": 555 },
          { "key": "FEES_TOTAL", "value": 0 },
          { "key": "DINER_GRAND_TOTAL", "value": 592 },
          { "key": "NON_TAXABLE_TOTAL", "value": 0 },
          { "key": "MERCHANT_SUB_TOTAL", "value": 555 }
        ]
      }
    ]
  },
  "editable": false,
  "catering": false,
  "group": false,
  "asap": true,
  "scheduled": false,
  "shared_order": false,
  "shared_order_host": false,
  "group_admin_cart": false,
  "expensed": false
}
```

## Acknowledgements

Portions of the authentication logic where reverse-engineered by
[@temminks](https://github.com/temminks)
[on StackOverflow](https://stackoverflow.com/a/62861527/408734).

## License

This project is licensed [under the LGPLv3 license](https://www.gnu.org/licenses/lgpl-3.0.en.html),
with the understanding that importing a Python modular is similar in spirit to dynamically linking
against it.

- You can use the library/CLI `grubhub` in any project, for any purpose,
  as long as you provide some acknowledgement to this original project for
  use of the library (for open source software, just explicitly including
  `grubhub` in the dependency such as a `pyproject.toml` or `Pipfile`
  is acknowledgement enough for me!).

- If you make improvements to `grubhub`, you are required to make those
  changes publicly available.
