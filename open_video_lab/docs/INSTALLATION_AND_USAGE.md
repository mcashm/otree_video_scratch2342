# Before you start

You will need to sign up for jitsi as a service (jaas) from 8x8.com,  who provide the platform for the videoconferencing, 
create an API key and an RSA keypair.  See [8x8's developer documentations](https://developer.8x8.com/jaas/docs/api-keys-generate-add)
 for details.


# Installation

This app is an extension for oTree v5. You will need to have oTree installed in order to use this software.

You will need these additional python libraries in your environment: 

- PyJWT
- Cryptography

To install the manually, use the below pip command

```
pip install pyjwt[crypto]
```

Alternatively add them to your requirements.txt (untested)

> [!TIP]
> **Tested versions of dependencies**
>
> Only the versions of the libraries below have been tested.  If you are experiencing problems,
> please ensure that your versions of these python libraries match the below list. 
> ```
> otree==5.10.0
> PyJWT==2.9.0
> cryptography==43.0.0
> ```

Download this repository and copy and paste the `open_video_lab` folder into the project otree folder.


> [!Warning]
> TODO:
> - repackage the repo so that it is just the open_video_lab app, and it can be downloaded directly into the project folder with no copy and pasting necessary

# Configuration

To work with the 8x8 api that you set up in the [Before you start](#before-you-start) section, you will need to create some environment variables.  How you do this will depend on your operating system/the platform you are deploying to.  

On Windows, find "Edit the system environment variables" in your start menu, click the "Environment Variables..." button and add new environment variables as below.

On Linux and Mac, set the environment variables on the command line using `export ENV_NAME=env_value` where ENV_NAME and env_value are the name ("key" - not to be confused with your API Key) and value respectively. Setting thus, the variables will only last for the current login session.  To persist them, add to your .bashrc, .zshrc, or equivalent, or to the `activate` script if you launch otree in a python virtual environment.

If you are running the video lab on Heroku, configure the environment as [config vars](https://devcenter.heroku.com/articles/config-vars).


You will need to set three environment variables to enable the video lab:

| Name | Value |
| ---- | ----- |
| JAAS_APP_ID | The APP as shown in your JAAS dashboard on the 8x8 website. |
| JAAS_KEY_ID | The Key ID for the API Key you intend to use for the video lab, found the JAAS dashboard. |
| JAAS_PRIVATE_KEY | The full contents of the .pk private key file associated with this Key ID |




# Usage (Integration with oTree experiment)

Include `open_video_lab` at the start of the app_sequence for any experiment you want to use the functionality in.  These session configs will also need the keys
`magic_cookie` where you should put your own 8x8 app ID, `blurred_pages` where you list any pages where you want to blur the video conference (or a default empty list: "[]" - 
with the quotation marks, as this is data interpreted by the templates as json) and a `server_host` with the base URL your oTree instance runs at. 

For example:

```

SESSION_CONFIGS = [
    { "name": "jisti_initial_test",
      "display_name": "Initial 8x8 jitsi test",
      "app_sequence": ["open_video_lab", "public_goods_modified"],
      "num_demo_participants": 3,
      "magic_cookie": "[your 8x8 APP ID goes here]",
      "blurred_pages": ["public_goods_simple/Contribute",],
      "server_host": "https://otree.ludwig.wbs.ac.uk",
    },
]
```

All templates for ALL apps in the experiment need to inherit from `open_video_lab/Base.html` instead of `global/Page.html`.  i.e. replace the default `{{extends "global/Page.html" }}` in every template you create with the below

```
{{ extends "open_video_lab/Base.html" }}
```

> [!IMPORTANT]
> This step ensures that if a participant refreshes or closes their window, they will rejoin the video lab session.  If you miss this step, a participant that has moved on from the first pages of the app who refreshes their page will be presented with a 'normal' oTree window with no way back into the video lab


Likewise, all `Waitpages` need to use the `open_video_lab/BaseWaitPage.html` template, or inherit from this.  If you are creating your own `WaitPage` templates, use the same method as above.  Otherwise assign them within `__init__.py` for your app like in the below, for example. 

```
class ExampleWaitPage(WaitPage):
    template_name = 'open_video_lab/BaseWaitPage.html
```

