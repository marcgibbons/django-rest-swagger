YAML Docstring
====================
Docstring parser powered by YAML syntax

This parser allows you override some parts of automatic method inspection
behaviours.

Example: 
    
.. code-block:: python

    @api_view(["POST"])
    def foo_view(request):
        """
        Your docs
        ---
        # YAML (must be separated by `---`)

        type:
          name:
            required: true
            type: string
          url:
            required: false
            type: url
          created_at:
            required: true
            type: string
            format: date-time

        serializer: .serializers.FooSerializer
        omit_serializer: false

        parameters_strategy: merge
        omit_parameters:
            - path
        parameters:
            - name: name
              description: Foobar long description goes here
              required: true
              type: string
              paramType: form
            - name: other_foo
              paramType: query
            - name: other_bar
              paramType: query
            - name: avatar
              type: file

        responseMessages:
            - code: 401
              message: Not authenticated
        """
        ...

parameters
--------------------------
Define parameters and its properties in docstrings:

.. code-block:: yaml

    parameters:
        - name: some_param
          description: Foobar long description goes here
          required: true
          type: integer
          paramType: form
        - name: other_foo
          paramType: query
        - name: avatar
          type: file

For the fields allowed in each parameter, see the 
`Parameter Object <https://github.com/swagger-api/swagger-spec/blob/master/versions/1.2.md#524-parameter-object>`_ 
fields and the 
`Data Type Fields <https://github.com/swagger-api/swagger-spec/blob/master/versions/1.2.md#433-data-type-fields>`_.

Exceptions: `$ref`, `items`, and `uniqueItems` are not currently supported.

It is possible to override parameters discovered by method inspector by
defining:
`parameters_strategy` option to either `merge` or `replace`

To define different strategies for different `paramType`'s use the
following syntax:

.. code-block:: yaml

    parameters_strategy:
        form: replace
        query: merge

By default strategy is set to `merge`


Sometimes the method inspector produces a list of parameters that
you might not want to see in SWAGGER form. To handle this situation
define `paramTypes` that should be omitted

.. code-block:: yaml

    omit_parameters:
        - form

Serializers
-------------------------

You can explicitly specify the serializer:

.. code-block:: yaml

    serializer: some.package.FooSerializer

`serializer` can take a relative path, or no path. Lookup begins in the 
module of the view:

.. code-block:: yaml

    serializer: .package.FooSerializer
    
    serializer: FooSerializer

You can specify different serializers for request and response:

.. code-block:: yaml

    request_serializer: some.package.FooSerializer
    response_serializer: some.package.BarSerializer

You can prevent django-rest-swagger from using any serializer:

.. code-block:: yaml

    omit_serializer: true


type
-----------------------
If your view does not use a serializer at all but instead outputs a simple
data type such as JSON you may define a custom response object in the method
signature as follows:

.. code-block:: yaml

    type:
      name:
        required: true
        type: string
      url:
        required: false
        type: url

responseMessages 
---------------------------------
To document error codes that your APIView might throw
you can define them in :code:`responseMessages`:

.. code-block:: yaml

    responseMessages:
        - code: 401
          message: Not authenticated
        - code: 403
          message: Insufficient rights to call this procedure


Different models for reading and writing operations
---------------------------------------------------
REST Framework does not output write_only fields in responses and also
does not require read_only fields to be provided. It is worth to
automatically register 2 separate models for reading and writing operations.

The discovered serializer will be registered with `Write` or `Read` prefix.
Response Class will be automatically adjusted if serializer class was
detected by method inspector.

You can also refer to this models in your parameters:

.. code-block:: yaml

    parameters:
        - name: CigarSerializer
          type: WriteCigarSerializer
          paramType: body


