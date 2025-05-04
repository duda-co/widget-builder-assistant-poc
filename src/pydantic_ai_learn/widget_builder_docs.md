## Here is the documentation of how to build widgets for the Duda platform:

The widget is combined of html with handlebars, javascript, css, content configuration and design configuration.

---

### HTML File instructions:

The HTML file should use Handlebars syntax and reference variables defined in the content configuration file using the syntax {{ variable name }}.
Texts, images, videos, icons should be replaced with handlebars variables so the site owner using the widget will be able to configure the text/image/video he would like to use.

These are the supported handlebar helpers:

**Accessing a variable**

`<div class="ex">{{headerText}}</div>`

| **Input Type** | **Additional Details** |
| --- | --- |
| Text |  |
| Dropdown | A String of the selected value. |
| Icon | String containing raw SVG markup. |
| Large Text | Requires the "triple-stash" `{{{` to avoid HTML escaping. |
| Image | String is an absolute URL of the image |
| Date | String formatted in standard universal full date-time pattern in the UTC timezone. |
| Radio Buttons | A String of the selected value. |
| Slider | A String of the selected value. |
| Video | Object with two fields: videoUrl and poster  |
| Audio | Object with three fields: url and name and uploadDate  |
| Checkbox |  |
| Toggle |  |

**If statement**

`If` statement checks if the value exists or is set to true. It will evaluate to false if it's an empty string, is false, or null. The `if` helper can only test for properties to be true or false – not arbitrary expressions. This is usually combined with a `Checkbox` or `Toggle` input.

Handlebars

`{{#if checkbox}}
	<p>Checkbox is selected / true</p>
{{else}}
	<p>Checkbox is not selected / false</p>
{{/if}}`

**Unless**

You can also use the `unless` handlebars helper, which is the inverse of `if`. This checks if the value is false.

Handlebars

`{{#unless toggle1}}
	<p>Toggle is disabled</p>
{{else}}
	<p>Toggle is enabled</p>
{{/unless}}`

**Equals**

You can use `equals` to define if a specific input equals a string.

Handlebars

`{{#equals dropDown "value1"}}
	<p>DropDown equals value1</p>
{{else}}
	<p>Dropdown does not equal value1</p>
{{/equals}}`

**Not Equals**

You can use `not equals` to define if a specific input does not equal a string.

Handlebars

`{{#notEquals dropDown "value1"}}
	<p>DropDown does not equal value1</p>
{{/notEquals}}`

**Decode**

Evaluate an input to check if it has a specific value. If they do, you can rewrite it to be a different value. This is great to use if you have a dropdown with many different options. It works by decoding an input, then checking if it equals a specific string. If it does, you can have it output a different string.

Handlebars

`{{#decode dropDown 
	"dropDownValue1" "Output this if value is dropDownValue1" 
	"dropDownValue2" "Output this if value is dropDownValue2"	"Default output" }}
{{/decode}}`

For example, if you had a dropdown named color with three entries (Red, Blue and Green), then you can use `decode` to get the output like this:

Handlebars

`{{#decode color 
	"Red" "My Favorite Color Is Red" 
	"Blue" "My Favorite Color Is Blue" 
	"Green" "My Favorite Color Is Green" "Default output" }}
{{/decode}}`

**Each**

`Each` allows you to loop through a list or array of items. This is always linked with the `List` input inside of Widget Builder. While looping through, you will have access to each inner item inside of the list.

Handlebars

`<ul>
{{#each list1}}
	<li>{{listInnerText}}</li>
{{/each}}
</ul>`

Inside of an `each` loop, you are able to access three data variables to aid in the logic and visual output of your widget. `@index` will display the current iteration of the loop, while the `@first` and `@last` variables are booleans compatible with the `{{#if}}` logic tag. The `@index` variable is zero-based, meaning its value will be zero on the first iteration of your loop, and increase by one for each subsequent iteration.

Handlebars

`<ul>
{{#each list1}}
	<li>
    {{#if @first}}First Item!{{/if}}
    {{@index}} {{listInnerText}}
    {{#if @last}}Last Item!{{/if}}
  </li>
{{/each}}
</ul>`

> 📘
> 
> 
> The `@index`, `@first` and `@last` data variables are only available inside of an `each` loop.
> 

If the widget needs to display a dynamic number of items, please use the each loop.
You can’t use {{ this }} to access content of an item, you need to use the variable name of an inner child defined within the list in the content configuration as defined below

**Links**

Links must be handled in a specific way within Duda websites. Duda allows users to choose only valid pages, popups, eCommerce, etc. Due to this, Duda controls the entire output of the anchor markup to automatically format it to perform the correct action when clicked. To use the input of a link, you must use the `custom_link` helper.

Handlebars

`{{#custom_link linkVariableName}}
	<span>Anchor Text or {{linkText}}</span>
{{/custom_link}}`

This will output as standard anchor markup:

HTML

`<a href=”/about” relevant_attribute=”value”>
	<span>Anchor Text or About Page</span>
</a>`

**Buttons**

Duda allows you to use our standard button. This allows you to add buttons as parts of widgets, or as a standalone button with additional features. The benefit of doing this is that the button will use Duda's standard classes and thus inherit all global styles for buttons on the website. You can also use the button input design type to easily add style settings for this specific button.

Handlebars

`{{#custom_button btnText class="button-class"}}
{{/custom_button}}`

> 
> 
> 
> In the example above, you can include a custom class on the button, so that in the design settings you can target that button easier.
> 

If you want the button to be a link as well, you can surround the button in the #custom_link helper as well.

Handlebars

`{{#custom_link linkVariableName}}
	{{#custom_button btnText class="button-class"}}
	{{/custom_button}}
{{/custom_link}}`

**String Contains**

A logic helper that allows you to check if a string that was input contains a specific string. If it's true, you can output a certain HTML element.

Handlebars

`{{#strContains variableName "test"}}
	Input variable contains "test"
{{else}}
	Input variable does not contain "test"
{{/strContains}}`

**String Replace**

Searches through an string that is input by the user and replaces part of it with a new string. Useful for trimming spaces or new lines from inputs into text boxes.

Handlebars

`{{#strReplace variableName "findString" "replaceWith"}}{{/strReplace}}`

**HTML Escaping**

By default, handlebars escapes the output of any content added to the widget configuration. If you want to avoid escaping and directly embed the content in the page, you can use the triple-stash output: `{{{exampleVariable}}}`. This is good to use with large text inputs, as you might want to allow users to enter spaces (

) or full HTML.

Handlebars

`<p>{{{largeText}}}</p>`

**Date Format**

A  helper that allows you to format date variables using all the formatting options such as MM/dd/yyyy.

Handlebars

`{{#formatDate variableName "MMM dd YYYY"}}
{{/formatDate}}`

---

### Javascript File instructions:

In the Javascript file, access a handlebar variable using data.config['variable name']. 

this is true if the variable was defined in a content section or in a design section.

There could be multiple of the same widget on the same page so avoid using id selector in the css and javascript files, always use class names or data attributes.

The javascript file is executed within a scope of a function with this signature: 

```jsx
function(element, data, api){
	// your code goes here
}
```

Don't add the function signature to the code, the code will be executed inside this function by the Duda platform.

Always wrap your code with the following function:

```jsx
window.dmAPI.runOnReady('nameSpace',() => {
// code goes here
)
```

In the javascript file,  always access elements under the root element of the widget, the root element is passed to the function as a parameter called “element”.
If you need to run the javascript code when the dom is ready, don't use document.addEventListener('DOMContentLoaded'). Instead, use window.dmAPI.runOnReady.

Don’t define local variables with the  names “data” “api” and “element” since these names are defined in the wrapping function by the system

If asked to use services such as weather, stocks, charts etc, try to use free services that don’t require an API Key unless asked otherwise. 
For example, for weather you can use **Open-Meteo,** for charts you can use **chart.js**

Make sure to load the scripts to those services in the javascript code since they are not included by default by the system.

Google maps tip - If asked to use Google Maps to find locations, make sure the “type” field in the request i a single string like “parking” or “restaurants” and not an array like [”parking”]

**Using Duda Javascript API**

The javascript file can use Duda’s Javascript API that allows accessing the site content library, collections, stores etc. Since the widget is running with a “dummy” site when developing it, in most cases those APIs will return empty result so better to provide default data in case the API doesn’t return any.

Here’s the documentation of the different APIs:

**Content Library API**

The Content Library API returns data from your site's business info, text and images using Javascript. This article will walk you through how to use the API.

**Usage**

The Content Library API needs to be initialized before data can be accessed.

JavaScript

`const contentLib = await dmAPI.loadContentLibrary();`

Once initialized, different object properties can be accessed directly. In the example below, we are accessing the primary location's address and custom site texts.

JavaScript

`//access different areas of the Content Library
const address = contentLib.location_data.address;

const customTexts = contentLib.site_texts.custom

customTexts.forEach((siteText) => {
    console.log(`${siteText.label}: ${siteText.text}`)
})`

## **Content Library Object**

| **Property** | **Description** |
| --- | --- |
| **location_data** *object* | Contains location-specific data for the primary location associated with a site. |
| **additional_locations** *object* | Contains location-specific data for any secondary/child locations associated with a site. |
| **site_texts** *object* | Contains the standard and custom text strings. Each field has a max length of 2000 characters. |
| **business_data** *object* | Contains the `name` of the business and the primary image `logo_url` of the website. |
| **site_images** *object* | Images that can be set and used within the design of the website. If you have the data, you should populate the alt value. |

**Location Specific Information**

The following fields are related to a specific location in the content library.

**location_data & additional_locations**

| **Property** | **Description** |
| --- | --- |
| **phones** *object[]* | Contains phone numbers for this location. The object allows for a friendly label name and the actual phone number. Note that there is no specific requirement for phone numbers, Duda will display this in the same format you submit it in. Max 80 characters each.[See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#phone). |
| **emails** *object[]* | Contains all email addresses associated with this location. The object allows for a friendly label name and the actual email address. Max 80 characters each.[See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#email). |
| **label** *string* | A simple name for this location. This is displayed in the Duda Content Library UI related to this location. Max 80 characters. |
| **schema** *object* | Details of the location/organizational schema that's generated. **Note: only available as a property for `location_data`, setting schema properties for `additional_locations` is not currently supported.** |
| **social_accounts** *object* | The profile name of this location's social networks. You must pass only the profile name/ID. Do not pass the full URL (e.g., https://wwwfacebook.com/duda). We support the following social networks: Facebook, Twitter, Yelp, Foursquare, Google Plus, Instagram, Youtube, Linkedin, Pinterest, Vimeo, RSS, Reddit, Trip Advisor & Snapchat.[See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#social_accounts). |
| **address** *object* | Contains all fields required to display an address: streetAddress, postalCode, region, city, country.[See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#address). |
| **address_geolocation** *string* | A geocode address string used to get LAT/LON from a geocoding map service. This is generated within the Duda Editor UI when searching for an address. **Note: You can't update the geolocation string via the API (you can only read it).** |
| **geo** *object* | An object containing the LAT and LON of the address. Duda will return this if we've identified an address in the editor for this location, but we will not automatically generate it. You can pass this if you know the exact LAT/LON. |
| **logo_url** *string* | A URL directly referencing the logo of this location. Must be a public URL and be served over HTTPS. |
| **business_hours** *object[]* | An array containing each day of the week and the hours that the location opens and closes. For each set of hours, you can pass an array of days: MON, TUE, WED, THU, FRI, SAT, SUN that applies to those hours. Open and close hours must be in 24HH:MM format. So, for example, 7:30 am would be: 07:30 and 5 pm would be 17:00. If the business is closed on a certain day, please omit it from the data set. If the business is open 24 hours a day, you should pass the hours as 00:00 to 24:00.[See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#business_hours). |

### **phone**

| **Property** | **Description** |
| --- | --- |
| **phoneNumber** *string* | A specific phone number. |
| **label**  *string* | A label to associate with the above phone number. |

### **email**

| **Property** | **Description** |
| --- | --- |
| **emailAddress** *string* | A specific email address. |
| **label** *string* | A label to associate with the above email address. |

### **schema**

| **Property** |  |
| --- | --- |
| **type** *string* | The type of LocalBusinessSchema for this business. [Full list of types can be found here.](https://developer.duda.co/docs/local-business-schema) |
| **custom_fields** *array of objects* | An array of objects with `name` and `value` properties for additional schema fields. [This allows you to add any schema fields that Duda does not support via the content library data.](https://developer.duda.co/docs/local-business-schema) |

### **social_accounts**

| **Property** | **Description** |
| --- | --- |
| **tripadvisor** *string* | A TripAdvisor page ID. Max 200 characters. |
| **youtube** *string* | A YouTube page ID. Max 50 characters. |
| **facebook** *string* | A Facebook page ID. Max 200 characters |
| **yelp** *string* | A Yelp page ID. Max 300 characters |
| **pinterest** *string* | A Pinterest page ID. Max 200 characters. |
| **linkedin** *string* | A Linkedin page ID. Max 200 characters. |
| **instagram** *string* | An Instagram page ID. Max 60 characters. |
| **snapchat** *string* | A Snapchat page ID. Max 30 characters. |
| **twitter** *string* | A Twitter/X page ID. Max 300 characters. |
| **rss** *string* | A link to the site's RSS feed. Max 2048 characters. |
| **vimeo** *string* | A Vimeo page ID. Max 200 characters |
| **reddit** *string* | A Reddit page ID. Max 200 characters |
| **foursquare** *string* | A Foursquare page ID. Max 200 characters |
| **google_my_business** *string* | A Google Business ID. Max 200 characters |
| **whatsapp** *string* | A WhatsApp ID. Max 50 characters |
| **tiktok** *string* | A TikTok ID. Max 50 characters |

### **address**

| **Property** | **Description** |
| --- | --- |
| **streetAddress** *string* | The business's street address. |
| **postalCode** *string* | The business's postal code. |
| **region** *string* | The region where the business is located. |
| **city** *string* | The city where the business is located. |
| **country** *string* | The counter where the business is located. |

### **geo**

| **Property** | **Description** |
| --- | --- |
| **longitude** *string* |  |
| **latitude** *string* |  |

### **business_hours**

| **Property** | **Description** |
| --- | --- |
| **days** *string[]* | [ "MON", "TUE", "WED", "THU", "FRI" ] |
| **open** *string* | The time the business opens. |
| **close** *string* | The time the business closes. |

## **Global Properties**

Below is website content that does not relate to a specific location. This is global data stored across the website.

| **Property** | **Description** |
| --- | --- |
| **business_data** *object* | Contains the `name` of the business, the primary `logo_url` and fields used to populate Duda's AI assistant. [See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#business_data) |
| **site_texts** *object* | Containing overview, services, about_us and custom text strings. Each field has a max length of 4000 characters. There is a limit of 200 `site_text` per site. [See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#site_texts) |
| **site_images** *object[]* | Images that can be set and used within the design of the website. If you have the data, you should populate the alt value. [See the section below for details](https://developer.duda.co/reference/site-content-content-library-object#site_images) |

### **business_data**

The business data object contains visible content for the site such as the name and logo of the business, and also contains data that is used by Duda's AI assistant to generate appropriate prompts

| **Property** | **Description** |
| --- | --- |
| **name** *string* | The name of the business. This field is required *if* you are also providing the AI assistant fields listed below. |
| **logo_url** *string* | A URL to the overall business logo. |
| **description** *string* | The description of the business. This field is used solely by the Duda AI Assistant to generate relevant prompts for AI content. Max 5000 characters |
| **category** *string* | The category of the business. This field is used solely by the Duda AI Assistant to generate relevant prompts for AI content. Max 500 characters |
| **service_area** *string* | The service area of the business. This field is used solely by the Duda AI Assistant to generate relevant prompts for AI content. Any description of a service area is allowed, and is not limited to a specific address. Max 500 characters |
| **tone_of_voice** *string enum* | One of CONVERSATIONAL, HUMOROUS, ENTHUSIASTIC, INFORMATIVE, PROFESSIONAL, WITTY or AUTHORITATIVE. This field is used solely by the Duda AI Assistant to generate relevant prompts for AI content. Any other value outside of the enum will result in a parse error. |

### **site_texts**

| **Property** | **Description** |
| --- | --- |
| **overview** *string* | Overview of the business. Up to 4000 characters. |
| **services** *string* | List of services. Up to 4000 characters. |
| **about_us** *string* | About the business. Up to 4000 characters. |
| **custom** *object[]* | An array of key/value pairs of custom text to be used as site content. Each object in the array consists of a `label` and `text` property. |

### **site_images**

| **Property** | **Description** |
| --- | --- |
| **label** *string* | Identifier for image in the content library. Used when connecting this image to widgets. Max 80 characters. |
| **url** *string* | A URL to the image. |
| **alt** *string* | A description of the image used by screen readers and other assistive technologies. Max 80 characters. |

**Example Payload**

JSON

```jsx
{
  "location_data":{
    "phones":[
      {
        "phoneNumber":"123-123-1234",
        "label":"Russ Phone"
      },
      {
        "phoneNumber":"18001234567",
        "label":"Duda Phone"
      }
    ],
    "emails":[
      {
        "emailAddress":"api@duda.co",
        "label":"API Email"
      },
      {
        "emailAddress":"support@duda.co",
        "label":"Support Email"
      }
    ],
    "schema": {
      "type": "Resort",
      "custom_fields":[
        {
          "name":"acceptsReservations",
          "value":true
        },
        {
          "name":"priceRange",
          "value":"$$$"
        }
      ]
    },
    "label":"Duda HQ",
    "social_accounts":{
      "tripadvisor":"Restaurant_Review-g32849-d2394400-Reviews-Oren_s_Hummus_Shop-Palo_Alto_California.html",
      "youtube":"UCPMwzOc1Su-s2z-J1xiU9ig",
      "facebook":"duda",
      "yelp":"orens-hummus-shop-palo-alto",
      "pinterest":"michelleobama",
      "google_plus":"+Dudamobile577",
      "linkedin":"duda",
      "instagram":"orenshummus",
      "snapchat":"michelleobama",
      "twitter":"dudamobile",
      "rss":"https://www.duda.co/blog/feed/",
      "vimeo":"dudamobile",
      "reddit":"duda"
    },
    "address":{
      "streetAddress":"577 College Ave",
      "postalCode":"94306",
      "region":"CA",
      "city":"Palo Alto",
      "country":"US"
    },
    "address_geolocation":"1833 Harvard St NW, Washington, DC 20009, USA",
    "geo":{
      "longitude":"-122.4757527166",
      "latitude":"37.502439189002"
    },
    "logo_url":"https://du-cdn.multiscreensite.com/duda_website/img/home/agencies.svg",
    "business_hours":[
      {
        "days":[
          "MON",
          "TUE",
          "WED",
          "THU",
          "FRI"
        ],
        "open":"09:00",
        "close":"18:00"
      }
    ]
  },
  "additional_locations":[
    {
      "uuid":"276169839",
      "phones":[
        {
          "phoneNumber":"123-123-1234",
          "label":""
        }
      ],
      "emails":[
        
      ],
      "label":"Duda Tel Aviv",
      "social_accounts":{
        
      },
      "address":{
        
      },
      "geo":{
        "longitude":"34.78337",
        "latitude":"32.07605"
      },
      "logo_url":null,
      "business_hours":null
    }
  ],
  "site_texts":{
    "overview":"Oh, Duda? Duda is a variation of \"Dude\", who just happens to be the main character in one of our favorite movies of all time: The Big Lebowski. You should watch it some time. Look out for that ferret!",
    "services":"- Responsive Website Builder",
    "custom":[
      {
        "label":"Example CTA 1",
        "text":"THE WEB DESIGN PLATFORM FOR Scaling Your Agency"
      },
      {
        "label":"Example CTA 2",
        "text":"THE WEB DESIGN PLATFORM FOR\nBuilding Websites Faster"
      }
    ],
    "about_us":"Duda is a leading website builder for web professionals and agencies of all sizes. Our website builder enables you to build amazing, feature-rich websites that are perfectly suited to desktop, tablet and mobile. Our mobile builder enables you to build mobile-only sites from scratch, or based on an existing desktop site or Facebook business page. Duda allows professionals and agencies to build high-converting, personalized websites at scale. Duda optimizes each and every site for Google PageSpeed."
  },
  "business_data":{
    "name":"Duda",
    "logo_url":"https://www.duda.co/developers/REST-API-Reference/images/duda.svg",
    "description": "A responsive website builder built for web professionals",
    "category": "Software",
    "service_area": "A 30 mile radius from Boulder, Colorado",
    "tone_of_voice": "CONVERSATIONAL"
  },
  "site_images":[
    {
      "label":"Example Store Logo",
      "url":"https://irt-cdn.multiscreensite.com/7536fe2010ed4f7ea68e21d0cb868e01/dms3rep/multi/ice_cream_logo_b_w-18-300x300.svg",
      "alt":"Example Store Logo"
    },
    {
      "label":"Example Store Banner",
      "url":"https://irt-cdn.multiscreensite.com/7536fe2010ed4f7ea68e21d0cb868e01/dms3rep/multi/sign_icecream_shop-1000x1108.jpg",
      "alt":"Example Store Banner"
    }
  ]
}
```

**Collections JS API**

The Collections API returns filtered, sorted, searched and paginated data from your [collections](https://developer.duda.co/docs/collections) using Javascript. This article will walk you through how to use the Collections API and all of its options.

**Usage**

In the interest of page speed, the Collections API is not included in the page until it is initialized using Duda's JavaScript API.

JavaScript

`var collection = await dmAPI.loadCollectionsAPI()`

Once the Collections API is initialized, it can be used to fetch, filter, sort, search and paginate collection data via chaining additional methods to the `data` method. At a minimum, you must pass the collection name to the `data` method, followed by calling the `get` method. This configuration will return a single page of results from the specified collection.

JavaScript

`await collection.data("collectionName").get()`

Each call to the `get` method makes an asynchronous network request. This method returns a promise, which will be resolved with data matching the query.

**Options**

The Collection API supports optional method chaining to add specific filtering, sorting, and pagination when querying data. Below is an example using all optional methods.

JavaScript

`await collection.data("collectionName")
		.where("<field>", "<operator>", "<value>")
		.orderBy("<field>","<direction>")
		.pageSize(20)
		.pageNumber(2)
		.get()`

**Paginating Items**

Pagination is handled with two methods:

| **Method Name** | **Type** | **Required** | **Notes** |
| --- | --- | --- | --- |
| pageSize | Int | No | Defaults to 50 items per page.Max size is 100 items per page. |
| pageNumber | Int | No | Defaults to 0. |

**Filtering Items**

Use the `.where()` method to filter the results using a provided comparison. Where takes three arguments:

| **Argument** | **Type** | **Required** | **Description** |
| --- | --- | --- | --- |
| field | String | Yes | The field in the collection. |
| operator | String | Yes | Available operators: EQ, IN, NE, NIN, GT, GTE, LT, LTE, BTWN. |
| value | String | Array | number | Yes | A value to compare. |

**Filter Operators**

The `.where()` method can utilize several different operators to filter fields based on their value. Certain operators can only be applied to fields of a specific data type.

| **Value** | **Field Data Type** | **Description** |
| --- | --- | --- |
| EQ | string, number | Checks if the field is equal to the supplied value. |
| IN | string, number | Checks if the field contains a value within the supplied **array**. |
| NE | string, number | Checks if the field is *not* equal to the supplied value. |
| NIN | string, number | Checks if the field is *not* a value within the supplied array. |
| GT | number | Checks if the field is greater than the supplied value. |
| GTE | number | Checks if the field is greater than or equal to the supplied value. |
| LT | number | Checks if the field is less than the supplied value. |
| LTE | number | Checks if the field is less than or equal to the supplied value. |
| BTWN | number | Combination of LTE and GTE for convenience. Check if the field is equal or between two values. Expects a list of exactly two values. |

**Sorting Items**

Use the `.orderBy()` method to sort the query results. Order by takes two arguments:

| **Argument** | **Type** | **Required** | **Notes** |
| --- | --- | --- | --- |
| field | String | Yes | The field name in the collection. |
| direction | String | No | Possible values are “asc” and “desc”. |

> 📘Supported field types
> 
> 
> You can sort by all collection field types
> 

**Searching collection**

Use the `.search()` method to search a collection.

JavaScript

`await collection.data("collectionName").search("<search_query>").get()`

- You can search for all `string` fields in a collection.
- Search is case insensitive.
- When searching in a collection, we check whether the search query is contained in any of the searchable fields in the collection.

**Returning Specific Item Properties**

Use the `.select()` method to only return the specific properties you need for the site or widget to function. This can improve performance for collections with a large number of properties per item. Provide each property name as a separate argument to the function.

**Code Examples**

Let's assume we're calling the API with a collection called `Team Collection`. The response for that collection would be as follows:

JSON

`[
    {
        "data": {
            "second_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/second_image_jane_smith.jpg",
            "About title": "I advise companies and NGOs in initiatives and campaigns",
            "Number": "(670)-390-7270",
            "Related Projects": [
                "Design",
                "Performance",
                "New Features"
            ],
            "Join Date": "2023-09-19T00:00",
            "main_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/main_image_jane_smith.jpg.jpg",
            "About description": "This is the text area for a paragraph describing this service. You may want to give examples of the service and who may be able to benefit from it.",
            "Work experience": "<b>2020-2021</b><br/>\nAdvisor, South Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2019-2020</b><br/>\nConsultant, North Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2018-2019</b><br/>\nProject manager, East Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.",
            "Title": "Product Manager",
            "email": "mymail@mail.com",
            "Name": "Jane Smith"
        },
        "page_item_url": "1_jane_smith"
    },
    {
        "data": {
            "second_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/second_image_john_brown.jpg",
            "About title": "I advise companies and NGOs in initiatives and campaigns",
            "Number": "(671)-390-7270",
            "Related Projects": [
                "New Features",
                "Performance",
                "Tech Debt"
            ],
            "Join Date": "2023-08-03T00:00",
            "main_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/main_image_john_brown.jpg",
            "About description": "This is the text area for a paragraph describing this service. You may want to give examples of the service and who may be able to benefit from it.",
            "Work experience": "<b>2019-2020</b><br/>\nAdvisor, South Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2019-2020</b><br/>\nConsultant, North Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2018-2019</b><br/>\nProject manager, East Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.",
            "Title": "Developer",
            "email": "mymail@mail.com",
            "Name": "John Brown"
        },
        "page_item_url": "2_john_brown"
    },
    {
        "data": {
            "second_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/second_image_helen_jameson.jpg",
            "About title": "I advise companies and NGOs in initiatives and campaigns",
            "Number": "(672)-390-7270",
            "Related Projects": [
                "Design",
                "New Features"
            ],
            "Join Date": "2023-09-30T00:00",
            "main_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/main_image_helen_jameson.jpg",
            "About description": "This is the text area for a paragraph describing this service. You may want to give examples of the service and who may be able to benefit from it.",
            "Work experience": "<b>2018-2019</b><br/>\nAdvisor, South Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2019-2020</b><br/>\nConsultant, North Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2018-2019</b><br/>\nProject manager, East Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.",
            "Title": "Designer",
            "email": "mymail@mail.com",
            "Name": "Helen Jameson"
        },
        "page_item_url": "3_helen_jameson"
    },
    {
        "data": {
            "second_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/second_image_tom_philips.jpg",
            "About title": "I advise companies and NGOs in initiatives and campaigns",
            "Number": "(673)-390-7270",
            "Related Projects": [
                "Tech Debt",
                "New Features"
            ],
            "Join Date": "2023-09-17T00:00",
            "main_image": "https://static-cdn.multiscreensite.com/dynamicpages/defaultCollection/Team_member/main_image_tom_philips.jpg",
            "About description": "This is the text area for a paragraph describing this service. You may want to give examples of the service and who may be able to benefit from it.",
            "Work experience": "<b>2022-2023</b><br/>\nAdvisor, South Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2019-2020</b><br/>\nConsultant, North Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.<br/><br/>\n<b>2018-2019</b><br/>\nProject manager, East Company<br/>\nIn this position, I led a team of more than 40 professional and volunteer staff members, from various company departments.",
            "Title": "QA Engineer",
            "email": "mymail@mail.com",
            "Name": "Tom Phillips"
        },
        "page_item_url": "4_tom_phillips"
    }
]`

**Getting the first row values**

JavaScript

```jsx
const coll = await collection.data("Team Collection").get();

console.log(coll.values[0].data);
```

**Getting a specific row**

JavaScript

`await collection.data("Team Collection").where("Name", "EQ", "John Brown").get()`

**Getting all rows that match a multi-select field**

JSON

`await collection.data("Team Collection").where("Related Projects", "IN", ["Design", "Performance"]).get()`

**Sorting by Date**

JSON

`await collection.data("Team Collection").sort("Join Date", "asc").get()`

**Store JS API**

Duda's native product catalog is built on top of the collection infrastructure.

This means that the product catalog can be filtered, sorted, searched and paginated in the same manner as the [Collections JS API](https://developer.duda.co/docs/collections-api).

**Intialization**

The Store JS API is initialized in the same manner as the Collections JS API

JavaScript

`dmAPI.loadCollectionsAPI().then(api => {
	// do something with API
})`

Once the collection has been initialized, use the method `storeData`.

- To access the product catalog, pass `catalog_product` as the collection name.
- To access the product categories, pass `catalog_category` as the collection name.

JavaScript

`api.storeData("catalog_product").get().then(data => {...})`

---

### Css File instructions:

There could be multiple of the same widget on the same page so avoid using id selector in the css and javascript files, always use class names or data attributes.

Important: You can use scss but you can’t access content or design variables in your css file!

In order to avoid conflicts with other elements that might be on the same document, wrap the entire scss in a block: 

```jsx
.{widgetClassName} {
	// all the generated scss code goes here
}
```

Remember that the {{widgetClassName}} classname is generated by the system in the html so DO NOT add it as a class to any of the html elements you generate and do not add it to any custom selector you use in the design configuration!!

---

### Content configuration file instructions:

The content file should be a json that specifies each handlebar variables you use in the html and javascript. 
The syntax should be:
{"sections":[{"sectionType":"type","id":"some id","attributeName":"variable name","config":{"label":"Text","placeholder":"","defaultValue":"some default value}}]}

Here is an example json with all supported content types and their configuration:

```jsx
"sections": [
      {
        "sectionType": "text",
        "id": "466d56d0-9102-58d5-1540-b549a019f811",
        "attributeName": "text1",
        "config": {
          "label": "Text",
          "placeholder": ""
        }
      },
      {
        "sectionType": "checkbox",
        "id": "d9ee787a-3fea-edaf-8669-da4b2c7bad89",
        "attributeName": "checkbox1",
        "config": {
          "label": "Checkbox"
        }
      },
      {
        "sectionType": "dropdown",
        "id": "94c95fa6-31eb-a393-4a35-d176684c80d7",
        "attributeName": "dropdown1",
        "config": {
          "options": [
            {
              "value": "value1",
              "label": "Label 1"
            },
            {
              "value": "value2",
              "label": "Label 2"
            }
          ],
          "label": "Dropdown"
        }
      },
      {
        "sectionType": "description",
        "id": "1da5669e-98bf-91e4-e547-7547fd4dc5b9",
        "config": {
          "label": "Description"
        }
      },
      {
        "sectionType": "divider",
        "id": "50ea7a7c-3e70-d2b6-0e40-124d244363f8",
        "config": {
          "label": "Divider"
        }
      },
      {
        "id": "e8650b5e-6e84-ee0f-de10-3035428d6305",
        "sectionType": "group",
        "attributeName": "group1",
        "config": {
          "sections": [
            {
              "sectionType": "text",
              "id": "085059df-5b5c-40c0-352f-ce9be5995932",
              "attributeName": "text2",
              "config": {
                "label": "Text",
                "placeholder": ""
              }
            }
          ],
          "label": "Group",
          "value": [
            {
              "sectionType": "new",
              "id": "085059df-5b5c-40c0-352f-ce9be5995932",
              "config": {
                "label": "New Section"
              }
            }
          ]
        },
        "label": "Group",
        "additionalText": "(group1)",
        "items": [
          {
            "id": "085059df-5b5c-40c0-352f-ce9be5995932",
            "sectionType": "text",
            "attributeName": "text2",
            "config": {
              "label": "Text"
            },
            "label": "Text",
            "additionalText": "(text2)",
            "items": [],
            "notInsertable": true,
            "onlyTopLevel": false
          }
        ],
        "notInsertable": false,
        "onlyTopLevel": true
      },
      {
        "sectionType": "icon",
        "id": "66029533-b13c-cd09-ee49-92c888b9580e",
        "attributeName": "icon1",
        "config": {
          "label": "Icon",
          "defaultValue": ""
        }
      },
      {
        "sectionType": "link",
        "id": "366f0923-be44-956e-aefe-4a445fe2b3fb",
        "attributeName": "link1",
        "config": {
          "layout": "sidebar",
          "label": "Link"
        }
      },
      {
        "sectionType": "largeText",
        "id": "948dc425-1342-0333-c446-38f7db6c20d0",
        "attributeName": "largeText1",
        "config": {
          "label": "Large Text",
          "placeholder": ""
        }
      },
      {
        "sectionType": "image",
        "id": "46d0c6d3-c1be-ad64-6737-eefaab56585c",
        "attributeName": "image1",
        "config": {
          "label": "Image"
        }
      },
      {
        "sectionType": "video",
        "id": "64d5bbe3-73e7-fb91-13a1-2045e03d3149",
        "attributeName": "video1",
        "config": {
          "label": "Video"
        }
      },
      {
        "sectionType": "audio",
        "id": "b21d1a10-9395-7536-cd43-e028c1f28a59",
        "attributeName": "audio1",
        "config": {
          "label": "Audio"
        }
      },
      {
        "sectionType": "date",
        "id": "bbeae868-8f21-2879-accb-f79136d949a6",
        "attributeName": "date1",
        "config": {
          "label": "Date",
          "selectedDateType": "select",
          "defaultValue": "2025-03-18T10:52:24.642Z"
        }
      },
      {
        "sectionType": "radio",
        "id": "8894f604-dcb3-e16a-4b94-3ac908162fa0",
        "attributeName": "radio1",
        "config": {
          "options": [
            {
              "value": "value1",
              "label": "Label 1"
            },
            {
              "value": "value2",
              "label": "Label 2"
            }
          ],
          "label": "Radio Buttons"
        }
      },
      {
        "sectionType": "toggle",
        "id": "f22d2a17-ee4b-53e5-11cb-b1ab56f20a96",
        "attributeName": "toggle1",
        "config": {
          "label": "Toggle"
        }
      },
      {
        "sectionType": "slider",
        "id": "c8808bdf-0850-3bb5-39a6-df9586c25aef",
        "attributeName": "slider1",
        "config": {
          "label": "Slider"
          "sizeUnitMin": 0,
          "sizeUnitMax": 100,
          "sizeUnit": "%" // size unit can be % or px
        }
      },
      {
        "id": "b9846d9c-d12e-3669-486a-ec8e063a22fd",
        "sectionType": "list",
        "attributeName": "list1",
        "config": {
          "sections": [
            {
              "sectionType": "text",
              "id": "e34b5efb-9834-2417-2bd6-783df8fddc60",
              "attributeName": "text3",
              "config": {
                "label": "Text",
                "placeholder": ""
              }
            }
          ],
          "defaultItems": "3",
          "addItemLabel": "Add Item",
          "label": "List",
          "value": [
            {
              "sectionType": "new",
              "id": "e34b5efb-9834-2417-2bd6-783df8fddc60",
              "config": {
                "label": "New Section"
              }
            }
          ]
        },
        "label": "List",
        "additionalText": "(list1)",
        "items": [
          {
            "id": "e34b5efb-9834-2417-2bd6-783df8fddc60",
            "sectionType": "text",
            "attributeName": "text3",
            "config": {
              "label": "Text"
            },
            "label": "Text",
            "additionalText": "(text3)",
            "items": [],
            "notInsertable": true,
            "onlyTopLevel": false
          }
        ],
        "notInsertable": false,
        "onlyTopLevel": true
      }
    ]
```

important - add defaultValue attribute for all sections beside “link”.
Don't add a defaultValue attribute for section of type "link"!

Make sure to add a default value to text, button, image and icon 

For image default value, please use this service: https://placehold.co/600x400 you can change the 600x400 according to the desired size.

You can use the “description” section to add texts to the widget editor in order to make it more understandable to the user. The description will not be displayed in the widget html itself

When using a slider, make sure it doesn’t exceed 1000 otherwise the UI of the slider will too width

important - list configuration should always have in the config a child called “sections” which is an array!!

---

### Design configuration file instructions:

The design file should contain a json with two type of sections:

1. Sections that control the css of widget elements using a css selector
2. Sections like in the content configuration that expose a variable you can use in the html and javascript. 

Here’s a json with all design configuration options

```jsx
"sections": [
      {
        "sectionType": "background",
        "id": "ecf82df6-a756-7b45-35fd-db2e2af48fd0",
        "config": {
          "label": "Background"
        },
        "customSelector": ".selector"
      },
      {
        "sectionType": "border",
        "id": "9c005605-61b9-df2e-981a-923b8c82b02f",
        "config": {
          "label": "Border"
        },
        "customSelector": ".selector"
      },
      {
        "sectionType": "button",
        "id": "e4a7b3ce-71bf-95fe-d87f-eb21b357d08a",
        "config": {
          "label": "Button"
        },
        "customSelector": ".selector"
      },
      {
        "sectionType": "colorPicker",
         "id": "icon-color",
        "config": {
          "label": "Icon Color",
          "useVariable": true // if true, a config variable will be exposed, if false, it will affect a css selector
          "attributeName": "colorPicker1" // only relevant is useVariable=true
          "defaultValue": "#000000",
          "cssAttribute": [
            "color", "fill"
          ] //specify which css attributes this control will change, only relevant if useVariable = false
           "customSelector": ".selector" //// only relevant is useVariable=false
        },
      
      {
        "sectionType": "cssSlider",
        "id": "186fdab6-7c28-ed1c-a567-f897355fb2b4",
        "config": {
          "label": "CSS Slider"
        }
      },
      {
        "sectionType": "description",
        "id": "43c692a4-ec37-1f4b-89e9-df2bd3322b06",
        "config": {
          "label": "Description"
        }
      },
      {
        "sectionType": "dimensions",
        "id": "e3954c0c-2831-b97a-7c85-718cdcad5ccb",
        "config": {
          "label": "Dimensions",
         
          "widthHeightDisplay": "both"  // can be width/height/both
        },
        "customSelector": ".selector"
      },
      {
        "sectionType": "divider",
        "id": "db94114d-7e71-8bc8-55d6-65955fcc22ca",
        "config": {
          "label": "Divider"
        }
      },
      {
        "sectionType": "imageDesign",
        "id": "aa719c30-de3c-de9c-4c59-33c388ce1d3e",
        "config": {
          "label": "Image Design"
        },
        "customSelector": ".selector"
      },
      {
        "sectionType": "roundedCorners",
        "id": "b6ccd179-e1de-a894-3e60-133315da6fc9",
        "config": {
          "label": "Rounded Corners"
        },
        "customSelector": ".selector"
      },
      {
        "sectionType": "textStyle",
        "id": "5c59bf75-4431-2690-6737-fbec54b7bb7b",
        "config": {
          "label": "Text Style"
        },
        "customSelector": ".selector"
      },
      {
        "sectionType": "pintoscreen",
        "id": "32317d35-61be-d750-ae03-0e2dc20a186f",
        "config": {
          "label": "Floating"
        }
      },
      {
        "sectionType": "slider",
        "id": "c8808bdf-0850-3bb5-39a6-df9586c25aef",
        "attributeName": "slider2",
        "config": {
          "label": "Slider"
          "sizeUnitMin": 0,
          "sizeUnitMax": 100,
          "sizeUnit": "%" // size unit can be % or px
        }
      }
    ]
```

make sure to add “dimension” design section to icons and “imageDesign” section to images

Note that icon is not an image therefore don’t add an imageDesign section to control an icon.

Important note regarding colorPicker section: if you need to pass a color in your javascript to an external service, make sure to add  **useVariable:true** in your colorPicker section and pass the color in your javascript using data.config['variable name']

If you need to change icon color, use the “fill” css property in the colorPicker 

For both content and design configuration, make sure you are not creating nested content and design fields. **sections** is the only child field of each content and design