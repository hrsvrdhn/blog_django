# Code Beautiful
> A blog app

Blog made in Django web framework in backend and Bootstrap in front. It also have newsletter feature. Have a look <a href="https://code-beautiful.herokuapp.com" target="_blank">CodeBeautiful</a>.

## Installation

OS X & Linux:

```sh
pip install -r requirements.txt
python manage.py runserver
```

## Development setup

Before running the app make sure you complete the following steps :-<br>
* Create a <strong>SENDGRID API</strong>.
* Copy the contents of <strong>settings/base.py</strong> and make a new file <strong>settings/local.py</strong>.
* Replace SENDGRID_API_KEY variable value with your created API.

## Contributing

1. Fork it (<https://github.com/hrsvrdhn/blog_django/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
