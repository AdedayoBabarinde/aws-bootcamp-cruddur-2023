

# Week 3 — Decentralized Authentication

## Required Homework

## Provision Amazon Cognito User Pool using AWS UI (Console)
-  I provisioned Amazon Cognito User Pool in the AWS console as required

## Install and Configure Amplify Client-Side Library for Amazon Congito.
### Installation
- Install AWS Amplify with --save option

```sh
npm i aws-amplify --save
```
### Configuration
- Passed my env vars(Environment variables) to `docker-compose` file to the `front-end` service

```yml
    REACT_APP_AWS_PROJECT_REGION: "${AWS_DEFAULT_REGION}"
    REACT_APP_AWS_COGNITO_REGION: "${AWS_DEFAULT_REGION}"
    REACT_APP_AWS_USER_POOLS_ID: "eu-west-2_FL5gh7PYx"
    REACT_APP_CLIENT_ID: "3big6mrdudlkj032q8sva42lkr"
```

- Linked cognito user pool to the code in  `App.js`
```js
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {}, // (optional) - Hosted UI configuration
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           // REQUIRED - Amazon Cognito Region
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: process.env.REACT_APP_CLIENT_ID,   // 
  }
});
```

## Show Some Components if You Are Logged in Only
- Implemented some components in these pages `HomeFeedPage.js`, `DesktopNavigation.js`, `ProfileInfo.js`, `DesktopSidebar.js`.
### HomeFeedPage.js
- Removed old cookies method for Auth.
```js
import { Auth } from 'aws-amplify';

// set a state (Already Done)
const [user, setUser] = React.useState(null);

// check if we are authenicated
const checkAuth = async () => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};

// check when the page loads if we are authenicated (Already Done)
React.useEffect(()=>{
  loadData();
  checkAuth();
}, [])
```
- We'll want to pass user to the following components: (Already Done)
```js
<DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
<DesktopSidebar user={user} />
```

### DesktopNavigation.js
- We'll rewrite `DesktopNavigation.js` so that it conditionally shows links in the left hand column
on whether you are logged in or not. (Already Done)

### ProfileInfo.js
- Removed old cookies method for Auth.
```js
import { Auth } from 'aws-amplify';

const signOut = async () => {
  try {
      await Auth.signOut({ global: true });
      window.location.href = "/"
  } catch (error) {
      console.log('error signing out: ', error);
  }
}
```

### DesktopSidebar.js
- Rewrote `DesktopSidebar.js` if conditions, to make the code clearer.
```js
  let trending;
  let suggested;
  let join;
  if (props.user) {
    trending = <TrendingSection trendings={trendings} />
    suggested = <SuggestedUsersSection users={users} />
  } else {
    join = <JoinSection />
  }
```

## Implement API Calls to Amazon Coginto for Custom Login, Signup, Recovery and Forgot Password Page

### Signin Page
- Removed old cookies method for Auth.
```js
import { Auth } from 'aws-amplify';

  const [errors, setErrors] = React.useState('');

  const onsubmit = async (event) => {
    setErrors('')
    event.preventDefault();
    Auth.signIn(email, password)
    .then(user => {
      localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
      window.location.href = "/"
    })
    .catch(error => { 
      if (error.code == 'UserNotConfirmedException') {
        window.location.href = "/confirm"
      }
      setErrors(error.message)
    });
    return false
  }
```
- Encountered an error when authenticating because the user created manually from AWS Cognito Console wasn't **"Verified"**
- Run this command to solve the issue (confirming the password)
```sh
aws cognito-idp admin-set-user-password --username 864ec250-50f1-70e9-9698-10aea66c0e5b --password Mololuwa12@- --user-pool-id eu-west-2_VVTlAbxEV --permanent
```

- Added **"name"** to our user manually form cognito console.<br>
![image](https://user-images.githubusercontent.com/50416701/226869053-50a3c1c3-a0ac-432f-b0e4-f7039fa0c643.png)


### Signup Page
- Clearly, we shouldn't be creating users by ourselves manually so we will create a signup page so that users can automatically signup and create content.
- Removed old cookies method for Auth.
```js
import { Auth } from 'aws-amplify';

const [errors, setErrors] = React.useState('');

const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('')
    console.log('username',username)
    console.log('email',email)
    console.log('name',name)
    try {
        const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
            name: name,
            email: email,
            preferred_username: username,
        },
        autoSignIn: { // optional - enables auto sign in after user is confirmed
            enabled: true,
        }
        });
        console.log(user);
        window.location.href = `/confirm?email=${email}`
    } catch (error) {
        console.log(error);
        setErrors(error.message)
    }
    return false
}
```

### ConfirmationPage
- Removed old cookies method for Auth.
```js
import { Auth } from 'aws-amplify';

const resend_code = async (event) => {
    setErrors('')
    try {
      await Auth.resendSignUp(email);
      console.log('code resent successfully');
      setCodeSent(true)
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err)
      if (err.message == 'Username cannot be empty'){
        setErrors("You need to provide an email in order to send Resend Activiation Code")   
      } else if (err.message == "Username/client id combination not found."){
        setErrors("Email is invalid or cannot be found.")   
      }
    }
}

const onsubmit = async (event) => {
    event.preventDefault();
    setErrors('')
    try {
      await Auth.confirmSignUp(email, code);
      window.location.href = "/"
      console.log("hey, your account is confirmed now go to the signin page and log in to see your home feedback.")
    } catch (error) {
      setErrors(error.message)
    }
    return false
  }
```

### Recovery Page
- Implemented Recovery Page
```js
import { Auth } from 'aws-amplify';

const onsubmit_send_code = async (event) => {
  event.preventDefault();
  setErrors('')
  Auth.forgotPassword(username)
  .then((data) => setFormState('confirm_code') )
  .catch((err) => setErrors(err.message) );
  return false
}

const onsubmit_confirm_code = async (event) => {
  event.preventDefault();
  setErrors('')
  if (password == passwordAgain){
    Auth.forgotPasswordSubmit(username, code, password)
    .then((data) => setFormState('success'))
    .catch((err) => setErrors(err.message) );
  } else {
    setErrors('Passwords do not match')
  }
  return false
}
```

## Authenticating Server Side
- Add in the `HomeFeedPage.js` a header to pass along the access token
```js
  headers: {
    Authorization: `Bearer ${localStorage.getItem("access_token")}`
  }
```

- Replace this code in `app.py` which will allow the Authorization header and expose it
```py
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
```
- Imported this library in `requirements.txt`
```txt
Flask-AWSCognito
```

- Used some code from this library `Flask-AWSCognito` that will handle auth with cognito serverside.
```py
# app.py
from lib.cognito_jwt_token import CognitoJwtToken, extract_access_token, TokenVerifyError

# Cognito Auth Serverside init
cognito_jwt_token = CognitoJwtToken(
  user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"), 
  user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region=os.getenv("AWS_DEFAULT_REGION")
)

def data_home():
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    # authenicatied request
    app.logger.debug("authenicated")
    app.logger.debug(claims)
    # to show who is the signed in user
    app.logger.debug(claims['username'])
    data = HomeActivities.run(cognito_user_id=claims['username'])
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    app.logger.debug("unauthenicated")
    data = HomeActivities.run()
  return data, 200
```

- Imported this file `cognito_jwt_token.py` from the library and edit it to work in our app

- Added this code to see if we're logged in by showing us more data in our `home feed page`
```py
# home_activities.py

# pass cognito_user_id to see if the user is auth.ed or not
def run(cognito_user_id=None):
# ...
# ...
      if cognito_user_id != None:
        extra_crud = {
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'Lore',
          'message': 'My dear brother, it the humans that are the problem',
          'created_at': (now - timedelta(hours=1)).isoformat(),
          'expires_at': (now + timedelta(hours=12)).isoformat(),
          'likes': 1042,
          'replies': []
        }
        results.insert(0,extra_crud)
```

- Added these two env vars to make our 3rd library work under back-end service in `docker-compose-gitpod.yml`
```yml
      AWS_COGNITO_USER_POOL_ID: "eu-west-2_****"
      AWS_COGNITO_USER_POOL_CLIENT_ID: "FL5gh7PYx****"
```

- Removed the access tocken after we sign out by adding this line to `ProfileInfo.js`
```js
    try {
        await Auth.signOut({ global: true });
        window.location.href = "/"
        localStorage.removeItem("access_token")
    }
```




