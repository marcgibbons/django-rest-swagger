# Change Log

## [2.1.2](https://github.com/marcgibbons/django-rest-swagger/tree/2.1.2) (2017-03-12)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.1.1...2.1.2)

**Implemented enhancements:**

- Make get\_swagger\_view\(\) AllowAny by default [\#592](https://github.com/marcgibbons/django-rest-swagger/issues/592)

**Closed issues:**

- Not showing comments as function description [\#622](https://github.com/marcgibbons/django-rest-swagger/issues/622)
- Authentication Error: UserView queryset attribute [\#621](https://github.com/marcgibbons/django-rest-swagger/issues/621)
- Django APIView serializer not being render [\#620](https://github.com/marcgibbons/django-rest-swagger/issues/620)
- Nested URLs not displaying correclty [\#618](https://github.com/marcgibbons/django-rest-swagger/issues/618)
- Using Regex Flags with DRS [\#602](https://github.com/marcgibbons/django-rest-swagger/issues/602)
- URL for swagger logo [\#601](https://github.com/marcgibbons/django-rest-swagger/issues/601)
- 403 when trying to access an empty documentation even as a Django superuser. [\#589](https://github.com/marcgibbons/django-rest-swagger/issues/589)
- Post parameters in not shown in swagger [\#588](https://github.com/marcgibbons/django-rest-swagger/issues/588)
- The UI does not render once djoser URLs are added  [\#584](https://github.com/marcgibbons/django-rest-swagger/issues/584)
- AssertionError when no endpoints are visible because of permissions [\#552](https://github.com/marcgibbons/django-rest-swagger/issues/552)

**Merged pull requests:**

- Add template block to override logo [\#624](https://github.com/marcgibbons/django-rest-swagger/pull/624) ([marcgibbons](https://github.com/marcgibbons))
- Add DRF 3.6, Python 3.6 to test suite [\#623](https://github.com/marcgibbons/django-rest-swagger/pull/623) ([marcgibbons](https://github.com/marcgibbons))
- Test against Django 1.11 [\#610](https://github.com/marcgibbons/django-rest-swagger/pull/610) ([edmorley](https://github.com/edmorley))
- Release/2.1.1 [\#606](https://github.com/marcgibbons/django-rest-swagger/pull/606) ([marcgibbons](https://github.com/marcgibbons))

## [2.1.1](https://github.com/marcgibbons/django-rest-swagger/tree/2.1.1) (2017-01-06)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.1.0...2.1.1)

**Implemented enhancements:**

- Anyway to set content-type for swagger docs? [\#529](https://github.com/marcgibbons/django-rest-swagger/issues/529)

**Closed issues:**

- Authorize button [\#600](https://github.com/marcgibbons/django-rest-swagger/issues/600)
- Document how to get 0.3 behaviour [\#596](https://github.com/marcgibbons/django-rest-swagger/issues/596)
- Bogus Models generated in schema [\#595](https://github.com/marcgibbons/django-rest-swagger/issues/595)
- Enable setting to toggle swagger UI [\#591](https://github.com/marcgibbons/django-rest-swagger/issues/591)
- Export the swagger definition [\#590](https://github.com/marcgibbons/django-rest-swagger/issues/590)
- It seems swagger get docs from another serializer of the same name. [\#587](https://github.com/marcgibbons/django-rest-swagger/issues/587)
- instance failed to match exactly one schema \(matched 0 out of 2\) [\#586](https://github.com/marcgibbons/django-rest-swagger/issues/586)
- OrderingFilter object has no attribute 'get\_schema\_fields' [\#585](https://github.com/marcgibbons/django-rest-swagger/issues/585)
- TypeError: \_\_new\_\_\(\) got an unexpected keyword argument 'type' [\#582](https://github.com/marcgibbons/django-rest-swagger/issues/582)
- Error with custom user model [\#579](https://github.com/marcgibbons/django-rest-swagger/issues/579)
- why swagger\_settings in settings.py is not work? [\#577](https://github.com/marcgibbons/django-rest-swagger/issues/577)
- AttributeError: 'NoneType' object has no attribute 'update' [\#555](https://github.com/marcgibbons/django-rest-swagger/issues/555)
- method self.request.version error [\#541](https://github.com/marcgibbons/django-rest-swagger/issues/541)
- Add block `extra\_scripts` to base.html template [\#539](https://github.com/marcgibbons/django-rest-swagger/issues/539)
- Method docstrings not included in generated docs [\#537](https://github.com/marcgibbons/django-rest-swagger/issues/537)
- Unable to generate Docs on model with ArrayField [\#403](https://github.com/marcgibbons/django-rest-swagger/issues/403)
- Add support for arrays as query parameters [\#312](https://github.com/marcgibbons/django-rest-swagger/issues/312)

**Merged pull requests:**

- Set zip\_safe as False [\#605](https://github.com/marcgibbons/django-rest-swagger/pull/605) ([jakul](https://github.com/jakul))
- @blueyed: doc api version authorization [\#598](https://github.com/marcgibbons/django-rest-swagger/pull/598) ([marcgibbons](https://github.com/marcgibbons))
- Restore swagger shortcut view [\#597](https://github.com/marcgibbons/django-rest-swagger/pull/597) ([marcgibbons](https://github.com/marcgibbons))
- optional urlconf [\#578](https://github.com/marcgibbons/django-rest-swagger/pull/578) ([theromis](https://github.com/theromis))
- Release 2.1.0 [\#576](https://github.com/marcgibbons/django-rest-swagger/pull/576) ([marcgibbons](https://github.com/marcgibbons))

## [2.1.0](https://github.com/marcgibbons/django-rest-swagger/tree/2.1.0) (2016-10-29)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.7...2.1.0)

**Closed issues:**

- How to force a DictField to be documented as an object, not a string? [\#568](https://github.com/marcgibbons/django-rest-swagger/issues/568)
- Load UI from a Swagger definition file [\#567](https://github.com/marcgibbons/django-rest-swagger/issues/567)
- Endpoint grouping/sorting is broken [\#536](https://github.com/marcgibbons/django-rest-swagger/issues/536)
- can't exclude urls in latest version? [\#530](https://github.com/marcgibbons/django-rest-swagger/issues/530)
- Issues with Schemas Generation [\#525](https://github.com/marcgibbons/django-rest-swagger/issues/525)
- URLs by router are not detected by swagger [\#479](https://github.com/marcgibbons/django-rest-swagger/issues/479)

**Merged pull requests:**

- simple fix in schema documentation [\#575](https://github.com/marcgibbons/django-rest-swagger/pull/575) ([drgarcia1986](https://github.com/drgarcia1986))
- 2.1.0: Make DRF 3.5 minimum version, use get\_schema\_view shortcut [\#570](https://github.com/marcgibbons/django-rest-swagger/pull/570) ([marcgibbons](https://github.com/marcgibbons))
- Minimum DRF version to 3.4.1 [\#566](https://github.com/marcgibbons/django-rest-swagger/pull/566) ([vinodc](https://github.com/vinodc))
- Release/2.0.7 [\#565](https://github.com/marcgibbons/django-rest-swagger/pull/565) ([marcgibbons](https://github.com/marcgibbons))

## [2.0.7](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.7) (2016-10-16)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.6...2.0.7)

**Closed issues:**

- All urls are not mapped by swagger [\#562](https://github.com/marcgibbons/django-rest-swagger/issues/562)
- Annotation order breaks doc generation [\#560](https://github.com/marcgibbons/django-rest-swagger/issues/560)
- Getting AssertionError: Expected a coreapi.Document when using format=openapi [\#547](https://github.com/marcgibbons/django-rest-swagger/issues/547)

**Merged pull requests:**

- Swagger doc view shortcut [\#564](https://github.com/marcgibbons/django-rest-swagger/pull/564) ([marcgibbons](https://github.com/marcgibbons))
- Extend OpenAPI codec to accept extra dict [\#563](https://github.com/marcgibbons/django-rest-swagger/pull/563) ([marcgibbons](https://github.com/marcgibbons))

## [2.0.6](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.6) (2016-10-02)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.5...2.0.6)

**Implemented enhancements:**

- UI Config Settings / Theming [\#347](https://github.com/marcgibbons/django-rest-swagger/issues/347)

**Closed issues:**

- Fail to parse urls correctly [\#551](https://github.com/marcgibbons/django-rest-swagger/issues/551)
- Swagger file [\#546](https://github.com/marcgibbons/django-rest-swagger/issues/546)
- Django 1.10 problem url [\#544](https://github.com/marcgibbons/django-rest-swagger/issues/544)
- No module named 'rest\_framework\_swagger.views' [\#543](https://github.com/marcgibbons/django-rest-swagger/issues/543)
- No module named 'rest\_framework\_swagger.views' [\#542](https://github.com/marcgibbons/django-rest-swagger/issues/542)
- How to use the new version \(2+\) with TokenAuthentication? [\#535](https://github.com/marcgibbons/django-rest-swagger/issues/535)
- OpenAPIRenderer raises AttributeError when the response object is not a Document [\#534](https://github.com/marcgibbons/django-rest-swagger/issues/534)
- Only one endpoint is shown in app [\#533](https://github.com/marcgibbons/django-rest-swagger/issues/533)
- run\_example.sh doesn't work without tweaking [\#524](https://github.com/marcgibbons/django-rest-swagger/issues/524)
- Group list\_route with viewset base path [\#515](https://github.com/marcgibbons/django-rest-swagger/issues/515)
- ReStructuredText - Summary breaks down when there's a class reference. [\#472](https://github.com/marcgibbons/django-rest-swagger/issues/472)
- API under / is not rendered properly  [\#446](https://github.com/marcgibbons/django-rest-swagger/issues/446)
- GeoDjango fields declared as string when type is GeoJSON [\#429](https://github.com/marcgibbons/django-rest-swagger/issues/429)
- docstring for nested JSON custom response [\#416](https://github.com/marcgibbons/django-rest-swagger/issues/416)
- reStructuredText docs not rendering [\#407](https://github.com/marcgibbons/django-rest-swagger/issues/407)
- displayed endpoint url list is not sorted [\#401](https://github.com/marcgibbons/django-rest-swagger/issues/401)
- Not able to show array with limited length info. [\#400](https://github.com/marcgibbons/django-rest-swagger/issues/400)
- custom RelatedField serializers shown as string [\#389](https://github.com/marcgibbons/django-rest-swagger/issues/389)
- Unable to navigate APis [\#384](https://github.com/marcgibbons/django-rest-swagger/issues/384)
- Unable to introspect fields.ListField [\#367](https://github.com/marcgibbons/django-rest-swagger/issues/367)
- Nested serializers: when combining form parameters and body, only body is sent. [\#360](https://github.com/marcgibbons/django-rest-swagger/issues/360)
- parameters\_strategy: replace fails with paramType: body [\#349](https://github.com/marcgibbons/django-rest-swagger/issues/349)
- Unable to POST on serializer fields  [\#346](https://github.com/marcgibbons/django-rest-swagger/issues/346)
- Nested many=True serializers? [\#335](https://github.com/marcgibbons/django-rest-swagger/issues/335)
- consumes/produces mieme types  [\#308](https://github.com/marcgibbons/django-rest-swagger/issues/308)
- Question: Does django-rest-swagger support complex response types?  [\#305](https://github.com/marcgibbons/django-rest-swagger/issues/305)
- Swagger not displaying fields when using get\_serializer\_class\(\) to return different serializers for different URL's [\#290](https://github.com/marcgibbons/django-rest-swagger/issues/290)

**Merged pull requests:**

- Add testing instructions \(Closes \#503\) [\#558](https://github.com/marcgibbons/django-rest-swagger/pull/558) ([marcgibbons](https://github.com/marcgibbons))
- PR \#554 [\#557](https://github.com/marcgibbons/django-rest-swagger/pull/557) ([marcgibbons](https://github.com/marcgibbons))
- Update dependency versions to latest. [\#556](https://github.com/marcgibbons/django-rest-swagger/pull/556) ([marcgibbons](https://github.com/marcgibbons))
- Docs fixup: METHOD -\> METHODS [\#550](https://github.com/marcgibbons/django-rest-swagger/pull/550) ([lwm](https://github.com/lwm))
- Release 2.0.6 [\#559](https://github.com/marcgibbons/django-rest-swagger/pull/559) ([marcgibbons](https://github.com/marcgibbons))
- Use minified swagger-ui.min.js [\#545](https://github.com/marcgibbons/django-rest-swagger/pull/545) ([coagulant](https://github.com/coagulant))

## [2.0.5](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.5) (2016-08-21)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.4...2.0.5)

**Implemented enhancements:**

- Add template blocks to allow customization [\#526](https://github.com/marcgibbons/django-rest-swagger/issues/526)

**Closed issues:**

- Should be a way to customize request serializer field type [\#355](https://github.com/marcgibbons/django-rest-swagger/issues/355)

**Merged pull requests:**

- Use entrypoint for Dockerfile \#524. [\#532](https://github.com/marcgibbons/django-rest-swagger/pull/532) ([marcgibbons](https://github.com/marcgibbons))
- Feature/526 template overrides [\#531](https://github.com/marcgibbons/django-rest-swagger/pull/531) ([marcgibbons](https://github.com/marcgibbons))
- run\_example: fix "docker build" command [\#527](https://github.com/marcgibbons/django-rest-swagger/pull/527) ([blueyed](https://github.com/blueyed))
- Feature: exception handling [\#523](https://github.com/marcgibbons/django-rest-swagger/pull/523) ([marcgibbons](https://github.com/marcgibbons))
- Release/2.0.4 [\#521](https://github.com/marcgibbons/django-rest-swagger/pull/521) ([marcgibbons](https://github.com/marcgibbons))

## [2.0.4](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.4) (2016-08-16)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.3...2.0.4)

**Implemented enhancements:**

- How to sort endpoints? [\#512](https://github.com/marcgibbons/django-rest-swagger/issues/512)
- How to control doc expansion in django-rest-swagger v2? [\#507](https://github.com/marcgibbons/django-rest-swagger/issues/507)

**Fixed bugs:**

- Django 1.10 TypeError at /api/docs/ argument of type 'NoneType' is not iterable [\#517](https://github.com/marcgibbons/django-rest-swagger/issues/517)

**Closed issues:**

- URLs not grouping together in 2.0 [\#518](https://github.com/marcgibbons/django-rest-swagger/issues/518)
- The raw json generated from django swagger fails when validated using swagger-tools [\#504](https://github.com/marcgibbons/django-rest-swagger/issues/504)
- Exception rendering swagger format \(2.0.3\) [\#502](https://github.com/marcgibbons/django-rest-swagger/issues/502)
- function based views cause get\_serializer\_class error [\#501](https://github.com/marcgibbons/django-rest-swagger/issues/501)
- The swagger urls are not using the SCRIPT\_NAME header [\#494](https://github.com/marcgibbons/django-rest-swagger/issues/494)
- @list\_route\(\) no collected [\#488](https://github.com/marcgibbons/django-rest-swagger/issues/488)
- Django Swagger shown HTTP Error 500 and not processed HTML code when accessing without logged in user [\#486](https://github.com/marcgibbons/django-rest-swagger/issues/486)
- 'LogoutView' object has no attribute 'get\_serializer\_class' [\#483](https://github.com/marcgibbons/django-rest-swagger/issues/483)
- Error in host [\#482](https://github.com/marcgibbons/django-rest-swagger/issues/482)
- Request Object is immutable while passing parameters through Swagger UI [\#473](https://github.com/marcgibbons/django-rest-swagger/issues/473)
- Invalid serializer with detail\_route and serializer\_class override [\#466](https://github.com/marcgibbons/django-rest-swagger/issues/466)

**Merged pull requests:**

- Feature/517 fix bug when auth urls none [\#520](https://github.com/marcgibbons/django-rest-swagger/pull/520) ([marcgibbons](https://github.com/marcgibbons))
- Add basic UI settings [\#519](https://github.com/marcgibbons/django-rest-swagger/pull/519) ([marcgibbons](https://github.com/marcgibbons))
- Feature/auto detect hosts [\#516](https://github.com/marcgibbons/django-rest-swagger/pull/516) ([marcgibbons](https://github.com/marcgibbons))
- Upgrade template settings for 1.10 support in example app. [\#514](https://github.com/marcgibbons/django-rest-swagger/pull/514) ([marcgibbons](https://github.com/marcgibbons))
- Update test env settings. [\#513](https://github.com/marcgibbons/django-rest-swagger/pull/513) ([marcgibbons](https://github.com/marcgibbons))
- Heroku deployment of example\_app. [\#506](https://github.com/marcgibbons/django-rest-swagger/pull/506) ([marcgibbons](https://github.com/marcgibbons))
- 2.0.3 release [\#500](https://github.com/marcgibbons/django-rest-swagger/pull/500) ([marcgibbons](https://github.com/marcgibbons))

## [2.0.3](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.3) (2016-07-24)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.2...2.0.3)

**Implemented enhancements:**

- Add LOGIN\_URL, LOGOUT\_URL to SWAGGER\_SETTINGS [\#480](https://github.com/marcgibbons/django-rest-swagger/issues/480)

**Closed issues:**

- UI does not show descriptions and response model from function based api views [\#496](https://github.com/marcgibbons/django-rest-swagger/issues/496)
- yaml specifications in \_\_pydoc\_\_ are ignored [\#492](https://github.com/marcgibbons/django-rest-swagger/issues/492)
- Whitenoise collectstatic fails due to nonexistent file [\#489](https://github.com/marcgibbons/django-rest-swagger/issues/489)

**Merged pull requests:**

- Feature/auth urls [\#499](https://github.com/marcgibbons/django-rest-swagger/pull/499) ([marcgibbons](https://github.com/marcgibbons))

## [2.0.2](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.2) (2016-07-20)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.10...2.0.2)

## [0.3.10](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.10) (2016-07-20)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.9...0.3.10)

**Closed issues:**

- ImportError: cannot import name duration\_string \(DRF 3.4.0\) [\#476](https://github.com/marcgibbons/django-rest-swagger/issues/476)
- How to represent a dictionary for Swagger UI [\#474](https://github.com/marcgibbons/django-rest-swagger/issues/474)
- Is django version 1.7.1 necessary? [\#471](https://github.com/marcgibbons/django-rest-swagger/issues/471)
- Wrong choices for duration field [\#469](https://github.com/marcgibbons/django-rest-swagger/issues/469)
- Enabling explicit swagger style model definition in yaml string [\#468](https://github.com/marcgibbons/django-rest-swagger/issues/468)
- Change the name in 'Response Class' -\> 'Model' [\#463](https://github.com/marcgibbons/django-rest-swagger/issues/463)
- Allow to set Selialiser name in documentation [\#458](https://github.com/marcgibbons/django-rest-swagger/issues/458)
- `request\_serializer` option doesn't work for GET queries [\#455](https://github.com/marcgibbons/django-rest-swagger/issues/455)
- Separate docs for separate groups of apps. [\#454](https://github.com/marcgibbons/django-rest-swagger/issues/454)
- REST framework 3.4 - Schema generation. [\#453](https://github.com/marcgibbons/django-rest-swagger/issues/453)
- Empty {% static %} tag in base.html leads to errors with django-storages [\#447](https://github.com/marcgibbons/django-rest-swagger/issues/447)
- How can I change the documented type of a SerializerMethodField? [\#445](https://github.com/marcgibbons/django-rest-swagger/issues/445)
- pytype for array [\#442](https://github.com/marcgibbons/django-rest-swagger/issues/442)
- Documentation output in markdown [\#441](https://github.com/marcgibbons/django-rest-swagger/issues/441)
- File parameters hard coded to body [\#437](https://github.com/marcgibbons/django-rest-swagger/issues/437)
- swagger not show when view have custom decorator [\#426](https://github.com/marcgibbons/django-rest-swagger/issues/426)
- How to skip documentation for some view functions [\#418](https://github.com/marcgibbons/django-rest-swagger/issues/418)
- AttributeError: 'CreateOnlyDefault' object has no attribute 'is\_update' [\#417](https://github.com/marcgibbons/django-rest-swagger/issues/417)
- Authorizations Object [\#415](https://github.com/marcgibbons/django-rest-swagger/issues/415)
- Use ListSerializer with `'CharField' object has no attribute 'get\_fields'` error [\#413](https://github.com/marcgibbons/django-rest-swagger/issues/413)
- Problem with custom CSRF cookie name [\#412](https://github.com/marcgibbons/django-rest-swagger/issues/412)
- YAML commands not being documented [\#411](https://github.com/marcgibbons/django-rest-swagger/issues/411)
- Support for custom routers [\#408](https://github.com/marcgibbons/django-rest-swagger/issues/408)
- How to show my REST APIs by rest\_framework\_swagger? [\#402](https://github.com/marcgibbons/django-rest-swagger/issues/402)
- paramType leads to incorrect input parameters for endpoint documentation [\#399](https://github.com/marcgibbons/django-rest-swagger/issues/399)
- Context \(inc request\) should be passed to serializer in introspection [\#397](https://github.com/marcgibbons/django-rest-swagger/issues/397)
- Multiple response type: docstring tags break [\#396](https://github.com/marcgibbons/django-rest-swagger/issues/396)
- Make a release for Django 1.9 full support [\#395](https://github.com/marcgibbons/django-rest-swagger/issues/395)
- Read only API in documentation? [\#394](https://github.com/marcgibbons/django-rest-swagger/issues/394)
- Upgrading this package breaks existing setup because of the required package definitions [\#391](https://github.com/marcgibbons/django-rest-swagger/issues/391)
- 'choice' field description uses the key [\#388](https://github.com/marcgibbons/django-rest-swagger/issues/388)
- Override introspection? [\#385](https://github.com/marcgibbons/django-rest-swagger/issues/385)
- Should query params from filter appear in methods other than GET \(list\)? [\#377](https://github.com/marcgibbons/django-rest-swagger/issues/377)
- Try it out creates duplicate Request URLS [\#376](https://github.com/marcgibbons/django-rest-swagger/issues/376)
- Consistent ValueError in 0.3.4 when used with a HashedFilesMixin-based class as STATICFILES\_STORAGE [\#375](https://github.com/marcgibbons/django-rest-swagger/issues/375)
- ModelViewSet documentation [\#374](https://github.com/marcgibbons/django-rest-swagger/issues/374)
- Authorization support? [\#372](https://github.com/marcgibbons/django-rest-swagger/issues/372)
- API Documentation is not available for only staff users  [\#369](https://github.com/marcgibbons/django-rest-swagger/issues/369)
- How to look for APIs via HTTPS [\#363](https://github.com/marcgibbons/django-rest-swagger/issues/363)
- Foreign key fields are represented as 'string', instead of 'field'. [\#361](https://github.com/marcgibbons/django-rest-swagger/issues/361)
- cannot implements read-only baseserializer because get\_fields method is required [\#358](https://github.com/marcgibbons/django-rest-swagger/issues/358)
- How to add custom endpoint  [\#354](https://github.com/marcgibbons/django-rest-swagger/issues/354)
- Add "include\_namespaces" as a setting variable [\#353](https://github.com/marcgibbons/django-rest-swagger/issues/353)
- Can't get this error to go away on GenericAPIView [\#351](https://github.com/marcgibbons/django-rest-swagger/issues/351)
- Google Fonts and Remote Sources [\#350](https://github.com/marcgibbons/django-rest-swagger/issues/350)
- exclude\_namespaces is ignored for related endpoints [\#348](https://github.com/marcgibbons/django-rest-swagger/issues/348)
- Django REST Swagger shows only {version} [\#344](https://github.com/marcgibbons/django-rest-swagger/issues/344)
- Wrongly recognized Django url pattern [\#342](https://github.com/marcgibbons/django-rest-swagger/issues/342)
- getting error "csrf failed while making POST request with an image file" [\#339](https://github.com/marcgibbons/django-rest-swagger/issues/339)
- Issue including markdown tables in docs [\#337](https://github.com/marcgibbons/django-rest-swagger/issues/337)
- Adding DynamicFieldsMixin causes KeyError 'request' [\#328](https://github.com/marcgibbons/django-rest-swagger/issues/328)
- Add `include\_namespaces` setting [\#327](https://github.com/marcgibbons/django-rest-swagger/issues/327)
- is\_superuser permission should be user.is\_staff [\#315](https://github.com/marcgibbons/django-rest-swagger/issues/315)
- \[Question\] Nested results/requests? [\#314](https://github.com/marcgibbons/django-rest-swagger/issues/314)
- Source of the image throbber.gif is wrong [\#311](https://github.com/marcgibbons/django-rest-swagger/issues/311)
- Use latest swagger-ui [\#309](https://github.com/marcgibbons/django-rest-swagger/issues/309)
- Specifying method overrides in docstring is now broken [\#303](https://github.com/marcgibbons/django-rest-swagger/issues/303)
- switch to pytest ? [\#292](https://github.com/marcgibbons/django-rest-swagger/issues/292)
- ViewSets and @detail\_route [\#288](https://github.com/marcgibbons/django-rest-swagger/issues/288)
- build\_form\_parameters does not handle complex types [\#276](https://github.com/marcgibbons/django-rest-swagger/issues/276)
- Support for Expressing Binary Return Types [\#275](https://github.com/marcgibbons/django-rest-swagger/issues/275)
- \_get\_method\_serializer should check dock\_parser before calling get\_response\_serializer\_class [\#274](https://github.com/marcgibbons/django-rest-swagger/issues/274)
- Question: How to keep YAML stuff  separate from docstring in django project because it makes file bulky?? [\#273](https://github.com/marcgibbons/django-rest-swagger/issues/273)
- Include Css source files \(less or scss\)? [\#272](https://github.com/marcgibbons/django-rest-swagger/issues/272)
- Django rest swagger views.py only uses first default renderer class [\#271](https://github.com/marcgibbons/django-rest-swagger/issues/271)
- Model Required List not Correctly Set based on Properties [\#270](https://github.com/marcgibbons/django-rest-swagger/issues/270)
- create\_view should create DRF Request not Django HttpRequest [\#269](https://github.com/marcgibbons/django-rest-swagger/issues/269)
- Arrays Always Treated as Primitives [\#268](https://github.com/marcgibbons/django-rest-swagger/issues/268)
- Parameters Omitted if Empty List [\#267](https://github.com/marcgibbons/django-rest-swagger/issues/267)
- Duplicated Code in Parsing [\#265](https://github.com/marcgibbons/django-rest-swagger/issues/265)
- Unneeded basePath on Return Value for SwaggerResourcesView [\#264](https://github.com/marcgibbons/django-rest-swagger/issues/264)
- More documentation around api\_path [\#263](https://github.com/marcgibbons/django-rest-swagger/issues/263)
- More documentation around api-key [\#262](https://github.com/marcgibbons/django-rest-swagger/issues/262)
- Setting format in docstring YAML Doesn't Do Anything [\#259](https://github.com/marcgibbons/django-rest-swagger/issues/259)
- type and format are switched for datetimes and wrong for enum [\#258](https://github.com/marcgibbons/django-rest-swagger/issues/258)
- Add UUID type to get\_data\_type [\#256](https://github.com/marcgibbons/django-rest-swagger/issues/256)
- Specifying Parameter Type Resets Required [\#254](https://github.com/marcgibbons/django-rest-swagger/issues/254)
- Simple way of setting URL Parameter [\#253](https://github.com/marcgibbons/django-rest-swagger/issues/253)
- pytype not really documented [\#252](https://github.com/marcgibbons/django-rest-swagger/issues/252)
- Management Command [\#251](https://github.com/marcgibbons/django-rest-swagger/issues/251)
- Move to Swagger 2.0 [\#250](https://github.com/marcgibbons/django-rest-swagger/issues/250)
- Unable to display serializers.fields on swagger docs [\#238](https://github.com/marcgibbons/django-rest-swagger/issues/238)
- Exception using ModelViewSet + paginate\_by attribute [\#232](https://github.com/marcgibbons/django-rest-swagger/issues/232)
- Using of default instead of initial to pre-populate html fields [\#226](https://github.com/marcgibbons/django-rest-swagger/issues/226)
- BooleanField rendered as a select instead of a checkbox [\#225](https://github.com/marcgibbons/django-rest-swagger/issues/225)
- Swagger is always expecting model or serializers [\#222](https://github.com/marcgibbons/django-rest-swagger/issues/222)
- Documentation not available via HTTPS [\#220](https://github.com/marcgibbons/django-rest-swagger/issues/220)
- Query parameter not accessible within the 'create' function of ModelViewSet. [\#216](https://github.com/marcgibbons/django-rest-swagger/issues/216)
- Documenting a method for multiple HTTP methods. [\#214](https://github.com/marcgibbons/django-rest-swagger/issues/214)
- TemplateDoesNotExist at /docs/ rest\_framework\_swagger/index.html [\#210](https://github.com/marcgibbons/django-rest-swagger/issues/210)
- How to add array parameters type support in docstring? [\#204](https://github.com/marcgibbons/django-rest-swagger/issues/204)
- support PaginationSerializer [\#197](https://github.com/marcgibbons/django-rest-swagger/issues/197)
- Method description not being parsed [\#196](https://github.com/marcgibbons/django-rest-swagger/issues/196)
- problem of using swagger when I use the get\_serializer\_class\(\) for dynamic serializer based on the URL's charges [\#194](https://github.com/marcgibbons/django-rest-swagger/issues/194)
- AttributeError when use CurrentUserDefault [\#193](https://github.com/marcgibbons/django-rest-swagger/issues/193)
- api\_key not being sent [\#173](https://github.com/marcgibbons/django-rest-swagger/issues/173)
- Option to Allow Specification of App\(s\) To Generate Docs For [\#160](https://github.com/marcgibbons/django-rest-swagger/issues/160)
- yaml response type format is not ideal [\#151](https://github.com/marcgibbons/django-rest-swagger/issues/151)
- Hide unwanted not allowed\_methods [\#142](https://github.com/marcgibbons/django-rest-swagger/issues/142)
- Multiple Separate Doc Urls? [\#141](https://github.com/marcgibbons/django-rest-swagger/issues/141)
- Token Auth Endpoint [\#120](https://github.com/marcgibbons/django-rest-swagger/issues/120)
- Question: How to set Data Type when using custom parameters in the docstring? [\#114](https://github.com/marcgibbons/django-rest-swagger/issues/114)
- Question: How could api urls be better grouped? [\#107](https://github.com/marcgibbons/django-rest-swagger/issues/107)
- Troubles with api\_path [\#102](https://github.com/marcgibbons/django-rest-swagger/issues/102)
- Question: How to add 'header' parameters? [\#101](https://github.com/marcgibbons/django-rest-swagger/issues/101)
- Question: How do I specify a 'root' api path? [\#92](https://github.com/marcgibbons/django-rest-swagger/issues/92)
- Issue with reverse-proxied nginx + gunicorn + django setup [\#83](https://github.com/marcgibbons/django-rest-swagger/issues/83)
- Allow parameter documentation to span more than one line in the docstring [\#81](https://github.com/marcgibbons/django-rest-swagger/issues/81)
- Trying to load content from HTTP instead of HTTPS [\#77](https://github.com/marcgibbons/django-rest-swagger/issues/77)
- Add support for nested resources / URLs [\#76](https://github.com/marcgibbons/django-rest-swagger/issues/76)
- enabled\_methods not behaving as expected [\#73](https://github.com/marcgibbons/django-rest-swagger/issues/73)
- Actions with same prefix are erroneously grouped. [\#69](https://github.com/marcgibbons/django-rest-swagger/issues/69)
- How to comment single mixins method in a viewset for default methods \(create, destroy etc..\) [\#67](https://github.com/marcgibbons/django-rest-swagger/issues/67)
- How to avoid to list POST updates \(have only POST inserts\) [\#66](https://github.com/marcgibbons/django-rest-swagger/issues/66)
- Help text doesn't appear in swagger ui [\#62](https://github.com/marcgibbons/django-rest-swagger/issues/62)
- Use docstring of individual APIView methods [\#58](https://github.com/marcgibbons/django-rest-swagger/issues/58)
- How to show Response Class, Response Content Type, and Error Status Codes? [\#37](https://github.com/marcgibbons/django-rest-swagger/issues/37)
- Django 1.4 Compatibility [\#23](https://github.com/marcgibbons/django-rest-swagger/issues/23)
- Cannot load resource documentation [\#13](https://github.com/marcgibbons/django-rest-swagger/issues/13)

**Merged pull requests:**

- Support Release 0.3.10 [\#491](https://github.com/marcgibbons/django-rest-swagger/pull/491) ([marcgibbons](https://github.com/marcgibbons))
- 2.0.0a0 docs typo fixup [\#484](https://github.com/marcgibbons/django-rest-swagger/pull/484) ([lwm](https://github.com/lwm))

## [0.3.9](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.9) (2016-07-17)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.1...0.3.9)

**Implemented enhancements:**

- Add possibility of generating 'header' parameters [\#3](https://github.com/marcgibbons/django-rest-swagger/issues/3)
- Add generic filtering parameters [\#2](https://github.com/marcgibbons/django-rest-swagger/issues/2)
- Add permission classes as part of the implementation notes [\#1](https://github.com/marcgibbons/django-rest-swagger/issues/1)

**Closed issues:**

- ImportError: cannot import name 'OpenAPIRenderer' [\#478](https://github.com/marcgibbons/django-rest-swagger/issues/478)
- Swagger UI doesn't work in 2.0.0 [\#477](https://github.com/marcgibbons/django-rest-swagger/issues/477)
- CSRF cookie fails on HttpOnly [\#432](https://github.com/marcgibbons/django-rest-swagger/issues/432)

**Merged pull requests:**

- Release 0.3.9 [\#481](https://github.com/marcgibbons/django-rest-swagger/pull/481) ([marcgibbons](https://github.com/marcgibbons))

## [2.0.1](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.1) (2016-07-14)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.0...2.0.1)

**Closed issues:**

- Swagger 2.0 roadmap [\#443](https://github.com/marcgibbons/django-rest-swagger/issues/443)

## [2.0.0](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.0) (2016-07-14)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/2.0.0a0...2.0.0)

**Closed issues:**

- DRS docs break with CSP that blocks inline scripts [\#434](https://github.com/marcgibbons/django-rest-swagger/issues/434)

## [2.0.0a0](https://github.com/marcgibbons/django-rest-swagger/tree/2.0.0a0) (2016-07-14)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.8...2.0.0a0)

**Closed issues:**

- \#Not working on production deployed on aws. if debug is true works on localhost  else fails on localhost as well. [\#464](https://github.com/marcgibbons/django-rest-swagger/issues/464)

**Merged pull requests:**

- Release: 2.0.0a0 [\#470](https://github.com/marcgibbons/django-rest-swagger/pull/470) ([marcgibbons](https://github.com/marcgibbons))

## [0.3.8](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.8) (2016-06-27)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.7...0.3.8)

**Closed issues:**

- AssertionError: The `slug\_field` argument is required. [\#460](https://github.com/marcgibbons/django-rest-swagger/issues/460)
- Errors with Django 1.10 [\#452](https://github.com/marcgibbons/django-rest-swagger/issues/452)
- Opening the docs makes 2 requests for each endpoint [\#440](https://github.com/marcgibbons/django-rest-swagger/issues/440)
- Serializer Meta option read\_only\_fields is not respected [\#424](https://github.com/marcgibbons/django-rest-swagger/issues/424)
- django1.9 can not work in web browser [\#405](https://github.com/marcgibbons/django-rest-swagger/issues/405)

**Merged pull requests:**

- Fix child field instantiation with missing arguments [\#459](https://github.com/marcgibbons/django-rest-swagger/pull/459) ([daluege](https://github.com/daluege))
- Fixed support for Django 1.10 [\#456](https://github.com/marcgibbons/django-rest-swagger/pull/456) ([tarkatronic](https://github.com/tarkatronic))
- Update testing matrix [\#451](https://github.com/marcgibbons/django-rest-swagger/pull/451) ([edmorley](https://github.com/edmorley))
- Respect serializer.Meta.read\_only\_fields in introspector [\#450](https://github.com/marcgibbons/django-rest-swagger/pull/450) ([maroux](https://github.com/maroux))
- Convert readthedocs link for their .org -\> .io migration for hosted projects [\#449](https://github.com/marcgibbons/django-rest-swagger/pull/449) ([adamchainz](https://github.com/adamchainz))
- Primitive list fields 413 [\#444](https://github.com/marcgibbons/django-rest-swagger/pull/444) ([Bakuutin](https://github.com/Bakuutin))

## [0.3.7](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.7) (2016-05-18)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.6...0.3.7)

**Merged pull requests:**

- update readthedocs url [\#439](https://github.com/marcgibbons/django-rest-swagger/pull/439) ([ariovistus](https://github.com/ariovistus))
- Added support for array type responses [\#438](https://github.com/marcgibbons/django-rest-swagger/pull/438) ([MrTam](https://github.com/MrTam))
- Add support for making API paths relative to the specified api\_path setting [\#433](https://github.com/marcgibbons/django-rest-swagger/pull/433) ([MrTam](https://github.com/MrTam))

## [0.3.6](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.6) (2016-04-21)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.5...0.3.6)

**Closed issues:**

- Building a django-rest-swagger package for conda ? [\#410](https://github.com/marcgibbons/django-rest-swagger/issues/410)
- Update urlpatterns to be a list of django.conf.urls.url\(\) instances [\#387](https://github.com/marcgibbons/django-rest-swagger/issues/387)
- Provide wheel package on PyPI [\#373](https://github.com/marcgibbons/django-rest-swagger/issues/373)
- `choice` parameter type is not valid [\#343](https://github.com/marcgibbons/django-rest-swagger/issues/343)
- Instructions to run the tests [\#235](https://github.com/marcgibbons/django-rest-swagger/issues/235)
- No real documentation [\#219](https://github.com/marcgibbons/django-rest-swagger/issues/219)
- the example and tests seems too old now. not willing to run it. [\#211](https://github.com/marcgibbons/django-rest-swagger/issues/211)

**Merged pull requests:**

- Fix bug in Django 1.9 when using ListFields [\#431](https://github.com/marcgibbons/django-rest-swagger/pull/431) ([cleberzavadniak](https://github.com/cleberzavadniak))
- Fix Default List Args [\#430](https://github.com/marcgibbons/django-rest-swagger/pull/430) ([yuce](https://github.com/yuce))
- excluding urls and namespaces from resource-level view as well [\#428](https://github.com/marcgibbons/django-rest-swagger/pull/428) ([pwfff](https://github.com/pwfff))
- Fix \#343 [\#422](https://github.com/marcgibbons/django-rest-swagger/pull/422) ([ivanprjcts](https://github.com/ivanprjcts))
- add exclude\_url\_name for the option to ignore particular views [\#421](https://github.com/marcgibbons/django-rest-swagger/pull/421) ([igorpejic](https://github.com/igorpejic))

## [0.3.5](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.5) (2016-01-24)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.4...0.3.5)

**Closed issues:**

- swagger urls endpoint crashes when placed in url with regex capture  [\#382](https://github.com/marcgibbons/django-rest-swagger/issues/382)
- Django 1.8+ deprecation warning for urlpatterns in urls.py:10 [\#380](https://github.com/marcgibbons/django-rest-swagger/issues/380)
- Design & Implement REST API [\#378](https://github.com/marcgibbons/django-rest-swagger/issues/378)
- Authorizations Object in SWAGGER\_CONFIG [\#371](https://github.com/marcgibbons/django-rest-swagger/issues/371)
- Get a JSON definition file [\#364](https://github.com/marcgibbons/django-rest-swagger/issues/364)
- Problem while installing django-rest-swagger in virtualenv [\#357](https://github.com/marcgibbons/django-rest-swagger/issues/357)
- Problem with custom CSRF cookie name [\#316](https://github.com/marcgibbons/django-rest-swagger/issues/316)
- Django 1.8 Support [\#249](https://github.com/marcgibbons/django-rest-swagger/issues/249)
- Incorrect yaml docs rendering. [\#190](https://github.com/marcgibbons/django-rest-swagger/issues/190)

**Merged pull requests:**

- Respect django's CSRF\_COOKIE\_NAME setting [\#392](https://github.com/marcgibbons/django-rest-swagger/pull/392) ([teeberg](https://github.com/teeberg))
- Allow arbitrary arguments to get methods of swagger classes [\#383](https://github.com/marcgibbons/django-rest-swagger/pull/383) ([dtheodor](https://github.com/dtheodor))
- Use the new style urlpatterns syntax to fix Django deprecation warnings [\#381](https://github.com/marcgibbons/django-rest-swagger/pull/381) ([edmorley](https://github.com/edmorley))
- Handle DRF's AcceptHeaderVersioning: send version in Accept header [\#379](https://github.com/marcgibbons/django-rest-swagger/pull/379) ([blueyed](https://github.com/blueyed))
- Ensuring fields.ListField introspects as 'array' \#367 [\#368](https://github.com/marcgibbons/django-rest-swagger/pull/368) ([respondcreate](https://github.com/respondcreate))
- Allow user to configure AnonymousUser class [\#365](https://github.com/marcgibbons/django-rest-swagger/pull/365) ([rodcarroll](https://github.com/rodcarroll))
- Fix for Assertion errors introduced in 3.0.2 [\#352](https://github.com/marcgibbons/django-rest-swagger/pull/352) ([martyzz1](https://github.com/martyzz1))

## [0.3.4](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.4) (2015-08-20)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.3...0.3.4)

**Closed issues:**

- Can one generate a pdf or html using django-rest-swagger [\#345](https://github.com/marcgibbons/django-rest-swagger/issues/345)
- The comment can not be parsed when using decorator [\#341](https://github.com/marcgibbons/django-rest-swagger/issues/341)
- boolean type doesn't work properly [\#340](https://github.com/marcgibbons/django-rest-swagger/issues/340)
- Trying to upgrade django rest swagger upgrades Django to 1.8.3 forcefully [\#332](https://github.com/marcgibbons/django-rest-swagger/issues/332)
- resource\_access\_handler is not documented [\#330](https://github.com/marcgibbons/django-rest-swagger/issues/330)
- 0.3.3 build? [\#329](https://github.com/marcgibbons/django-rest-swagger/issues/329)
- `get\_default\_value\(\)` raises Attribute error for a field using `CurrentUserDefault` [\#317](https://github.com/marcgibbons/django-rest-swagger/issues/317)

**Merged pull requests:**

- Fix for https://github.com/marcgibbons/django-rest-swagger/issues/308 [\#338](https://github.com/marcgibbons/django-rest-swagger/pull/338) ([thinkt4nk](https://github.com/thinkt4nk))
- Prepare CurrentUserDefault like DRF would do it [\#336](https://github.com/marcgibbons/django-rest-swagger/pull/336) ([ticosax](https://github.com/ticosax))
- Update base.html [\#334](https://github.com/marcgibbons/django-rest-swagger/pull/334) ([veerbhan](https://github.com/veerbhan))

## [0.3.3](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.3) (2015-07-24)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.2...0.3.3)

**Closed issues:**

- No endpoint description with Nginx + uWSGI [\#313](https://github.com/marcgibbons/django-rest-swagger/issues/313)
- getting access-control-origin error [\#300](https://github.com/marcgibbons/django-rest-swagger/issues/300)
- methods \['retrieve'\] in class docstring are not in view methods \['list'\] [\#297](https://github.com/marcgibbons/django-rest-swagger/issues/297)
- Missing Comma from sample Settings configuration [\#295](https://github.com/marcgibbons/django-rest-swagger/issues/295)
- ViewSets @list\_route [\#289](https://github.com/marcgibbons/django-rest-swagger/issues/289)
- Add hide\_parameters in yaml config [\#279](https://github.com/marcgibbons/django-rest-swagger/issues/279)
- date-time spelled wrong [\#257](https://github.com/marcgibbons/django-rest-swagger/issues/257)
- Tests should use the swagger 1.2 JSON schema to validate JSON output [\#233](https://github.com/marcgibbons/django-rest-swagger/issues/233)

**Merged pull requests:**

- improve validity for old parameter spec [\#326](https://github.com/marcgibbons/django-rest-swagger/pull/326) ([ariovistus](https://github.com/ariovistus))
- Fix attribute name on field for minimum/maximum [\#325](https://github.com/marcgibbons/django-rest-swagger/pull/325) ([mverteuil](https://github.com/mverteuil))
- Handle ManyRelatedField type as an array of strings [\#324](https://github.com/marcgibbons/django-rest-swagger/pull/324) ([mverteuil](https://github.com/mverteuil))
- Fix enum output regression for choice fields [\#323](https://github.com/marcgibbons/django-rest-swagger/pull/323) ([mverteuil](https://github.com/mverteuil))
- add support for items and uniqueItems [\#322](https://github.com/marcgibbons/django-rest-swagger/pull/322) ([ariovistus](https://github.com/ariovistus))
- Adds jsonschema requirement [\#320](https://github.com/marcgibbons/django-rest-swagger/pull/320) ([mverteuil](https://github.com/mverteuil))
- Get serializer by request user [\#319](https://github.com/marcgibbons/django-rest-swagger/pull/319) ([mverteuil](https://github.com/mverteuil))
- Omit empty resources [\#318](https://github.com/marcgibbons/django-rest-swagger/pull/318) ([mverteuil](https://github.com/mverteuil))
- validate drs output against swagger schema [\#310](https://github.com/marcgibbons/django-rest-swagger/pull/310) ([ariovistus](https://github.com/ariovistus))
- Added resource access filter callback mechanism [\#307](https://github.com/marcgibbons/django-rest-swagger/pull/307) ([mverteuil](https://github.com/mverteuil))
- A less naive strategy for getting view closure var [\#306](https://github.com/marcgibbons/django-rest-swagger/pull/306) ([mverteuil](https://github.com/mverteuil))
- Revert "Restrict filtering for list views" [\#304](https://github.com/marcgibbons/django-rest-swagger/pull/304) ([ariovistus](https://github.com/ariovistus))
- Update docgenerator.py [\#302](https://github.com/marcgibbons/django-rest-swagger/pull/302) ([davidrenne](https://github.com/davidrenne))
- Add PyYAML to requirements list [\#301](https://github.com/marcgibbons/django-rest-swagger/pull/301) ([shieldwed](https://github.com/shieldwed))
- test for get\_introspector. [\#298](https://github.com/marcgibbons/django-rest-swagger/pull/298) ([ariovistus](https://github.com/ariovistus))
- comma! [\#296](https://github.com/marcgibbons/django-rest-swagger/pull/296) ([ariovistus](https://github.com/ariovistus))
- nose wasn't collecting test\_methods wrapped by @no\_markdown [\#294](https://github.com/marcgibbons/django-rest-swagger/pull/294) ([ticosax](https://github.com/ticosax))
- Only test with latest minor versions of DRF [\#293](https://github.com/marcgibbons/django-rest-swagger/pull/293) ([ticosax](https://github.com/ticosax))
- Restrict filtering for list views [\#291](https://github.com/marcgibbons/django-rest-swagger/pull/291) ([ticosax](https://github.com/ticosax))

## [0.3.2](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.2) (2015-06-06)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.1...0.3.2)

**Closed issues:**

- Remove `protocol` settings [\#286](https://github.com/marcgibbons/django-rest-swagger/issues/286)

**Merged pull requests:**

- Remove 'protocol' settings [\#287](https://github.com/marcgibbons/django-rest-swagger/pull/287) ([ticosax](https://github.com/ticosax))
- Add optional support for django\_filters third party package [\#285](https://github.com/marcgibbons/django-rest-swagger/pull/285) ([ticosax](https://github.com/ticosax))

## [0.3.1](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.1) (2015-06-04)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.3.0...0.3.1)

**Closed issues:**

- Can't use blocks of code  in notes with bash commands that have "long options" [\#282](https://github.com/marcgibbons/django-rest-swagger/issues/282)
- No files on PyPI \(0.3.0\) [\#281](https://github.com/marcgibbons/django-rest-swagger/issues/281)

**Merged pull requests:**

- sync parameter strip match with parameter syntax [\#284](https://github.com/marcgibbons/django-rest-swagger/pull/284) ([ariovistus](https://github.com/ariovistus))
- tests for pr \#215 [\#283](https://github.com/marcgibbons/django-rest-swagger/pull/283) ([ariovistus](https://github.com/ariovistus))
- Support manual setting of protocol and base\_path [\#215](https://github.com/marcgibbons/django-rest-swagger/pull/215) ([joshglick](https://github.com/joshglick))

## [0.3.0](https://github.com/marcgibbons/django-rest-swagger/tree/0.3.0) (2015-05-15)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.9...0.3.0)

**Closed issues:**

- import error with 'smart\_text' [\#237](https://github.com/marcgibbons/django-rest-swagger/issues/237)
- Method "nickname" generation is a function of viewset class [\#230](https://github.com/marcgibbons/django-rest-swagger/issues/230)
- Choices not displaying on documentation [\#229](https://github.com/marcgibbons/django-rest-swagger/issues/229)

**Merged pull requests:**

- release 0.3.0 [\#278](https://github.com/marcgibbons/django-rest-swagger/pull/278) ([ariovistus](https://github.com/ariovistus))
- Exclude HiddenField from parsed fields [\#266](https://github.com/marcgibbons/django-rest-swagger/pull/266) ([jasonpstewart](https://github.com/jasonpstewart))
- DFR 3.1.0 has deprecated the pagination parameters [\#261](https://github.com/marcgibbons/django-rest-swagger/pull/261) ([mochawich](https://github.com/mochawich))
- Add some blocks to the main template for fast customization [\#248](https://github.com/marcgibbons/django-rest-swagger/pull/248) ([eillarra](https://github.com/eillarra))
- strip notes [\#247](https://github.com/marcgibbons/django-rest-swagger/pull/247) ([ariovistus](https://github.com/ariovistus))
- Replaced django.utils.importlib with python importlib [\#246](https://github.com/marcgibbons/django-rest-swagger/pull/246) ([JonesChi](https://github.com/JonesChi))
- Fixed docgenerator to work with Choices fields \#229 [\#244](https://github.com/marcgibbons/django-rest-swagger/pull/244) ([jonzlin95](https://github.com/jonzlin95))
- Running tests [\#242](https://github.com/marcgibbons/django-rest-swagger/pull/242) ([duduklein](https://github.com/duduklein))
- tests for \#234 [\#241](https://github.com/marcgibbons/django-rest-swagger/pull/241) ([ariovistus](https://github.com/ariovistus))
- Ensure namespace is not None before comparison [\#240](https://github.com/marcgibbons/django-rest-swagger/pull/240) ([pquentin](https://github.com/pquentin))
- Pass 'suffix' to DRF's get\_view\_name, resolve view name getter via DRF's VIEW\_NAME\_FUNCTION setting. [\#236](https://github.com/marcgibbons/django-rest-swagger/pull/236) ([JASchilz](https://github.com/JASchilz))
- Fix wrong grouping of resources [\#234](https://github.com/marcgibbons/django-rest-swagger/pull/234) ([lukas-hetzenecker](https://github.com/lukas-hetzenecker))
- Tweaks to get swagger-codegen working [\#218](https://github.com/marcgibbons/django-rest-swagger/pull/218) ([BradWhittington](https://github.com/BradWhittington))

## [0.2.9](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.9) (2015-03-07)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.8...0.2.9)

**Closed issues:**

- actually requires django-rest-framework 2.4.0 [\#221](https://github.com/marcgibbons/django-rest-swagger/issues/221)
- view.paginate\_by is not a required attribute for ViewSet object in REST Framework [\#199](https://github.com/marcgibbons/django-rest-swagger/issues/199)
- Question: Custom page for the documentation generated [\#195](https://github.com/marcgibbons/django-rest-swagger/issues/195)
- Swagger POSTs with Content-Type application/x-www-form-urlencoded instead of application/json [\#131](https://github.com/marcgibbons/django-rest-swagger/issues/131)
- Support for reStructuredText in docstrings [\#126](https://github.com/marcgibbons/django-rest-swagger/issues/126)
- Throbber image hardcoded to /static/ [\#52](https://github.com/marcgibbons/django-rest-swagger/issues/52)
- Support for sending json object in raw post data [\#50](https://github.com/marcgibbons/django-rest-swagger/issues/50)

**Merged pull requests:**

- prepare for 0.2.9 [\#228](https://github.com/marcgibbons/django-rest-swagger/pull/228) ([ariovistus](https://github.com/ariovistus))
- add tests for \#190 [\#227](https://github.com/marcgibbons/django-rest-swagger/pull/227) ([ariovistus](https://github.com/ariovistus))
- Fix Swagger link on the README [\#223](https://github.com/marcgibbons/django-rest-swagger/pull/223) ([agonzalezro](https://github.com/agonzalezro))
- fix \#52 [\#217](https://github.com/marcgibbons/django-rest-swagger/pull/217) ([ariovistus](https://github.com/ariovistus))
- Improve CSS [\#213](https://github.com/marcgibbons/django-rest-swagger/pull/213) ([Situphen](https://github.com/Situphen))
- HEAD requests should look at query params by default [\#209](https://github.com/marcgibbons/django-rest-swagger/pull/209) ([ariovistus](https://github.com/ariovistus))
- maybe resolve issue 190 [\#208](https://github.com/marcgibbons/django-rest-swagger/pull/208) ([ariovistus](https://github.com/ariovistus))
- Auto-detect NullBooleanField as boolean value [\#206](https://github.com/marcgibbons/django-rest-swagger/pull/206) ([jstohner](https://github.com/jstohner))
- Don't try to import urlconf unless it's a string. [\#205](https://github.com/marcgibbons/django-rest-swagger/pull/205) ([zenoamaro](https://github.com/zenoamaro))
- Add check for paginate\_by attribute [\#200](https://github.com/marcgibbons/django-rest-swagger/pull/200) ([davidharrigan](https://github.com/davidharrigan))
- fix two typos and adjust some grammar [\#192](https://github.com/marcgibbons/django-rest-swagger/pull/192) ([erictheise](https://github.com/erictheise))

## [0.2.8](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.8) (2015-01-11)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.7...0.2.8)

**Implemented enhancements:**

- pagination parameter not automatically detected [\#182](https://github.com/marcgibbons/django-rest-swagger/issues/182)

**Closed issues:**

- How can I run the project? [\#187](https://github.com/marcgibbons/django-rest-swagger/issues/187)
- Unable to read api [\#183](https://github.com/marcgibbons/django-rest-swagger/issues/183)
- No action provided in get\_serializer\_class [\#119](https://github.com/marcgibbons/django-rest-swagger/issues/119)
- How to do a "real" POST [\#113](https://github.com/marcgibbons/django-rest-swagger/issues/113)
- DocumentationGenerator ignores serializer field labels [\#105](https://github.com/marcgibbons/django-rest-swagger/issues/105)
- Unable to read api [\#84](https://github.com/marcgibbons/django-rest-swagger/issues/84)

**Merged pull requests:**

- reStructuredText support [\#189](https://github.com/marcgibbons/django-rest-swagger/pull/189) ([ariovistus](https://github.com/ariovistus))
- use get\_view\_description, not raw .\_\_doc\_\_ access [\#188](https://github.com/marcgibbons/django-rest-swagger/pull/188) ([ariovistus](https://github.com/ariovistus))
- automatically add pagination params [\#186](https://github.com/marcgibbons/django-rest-swagger/pull/186) ([ariovistus](https://github.com/ariovistus))
- make pytype admissible field in parameter fields [\#185](https://github.com/marcgibbons/django-rest-swagger/pull/185) ([ariovistus](https://github.com/ariovistus))

## [0.2.7](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.7) (2014-12-31)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.6...0.2.7)

**Closed issues:**

- drf v3 support [\#152](https://github.com/marcgibbons/django-rest-swagger/issues/152)
- Issue when get\_serializer\_class  references "self.request.user" [\#86](https://github.com/marcgibbons/django-rest-swagger/issues/86)

**Merged pull requests:**

- fix \#86 and add view mocker [\#184](https://github.com/marcgibbons/django-rest-swagger/pull/184) ([ariovistus](https://github.com/ariovistus))
- readthedocs bling [\#181](https://github.com/marcgibbons/django-rest-swagger/pull/181) ([ariovistus](https://github.com/ariovistus))
- pypi bling [\#179](https://github.com/marcgibbons/django-rest-swagger/pull/179) ([ariovistus](https://github.com/ariovistus))
- Add Sphinx to docs requirements [\#178](https://github.com/marcgibbons/django-rest-swagger/pull/178) ([lorden](https://github.com/lorden))
- Allow dynamic urlconf to get api urls [\#157](https://github.com/marcgibbons/django-rest-swagger/pull/157) ([cwirz](https://github.com/cwirz))

## [0.2.6](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.6) (2014-12-13)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.5...0.2.6)

**Closed issues:**

- please use tags for releases. [\#174](https://github.com/marcgibbons/django-rest-swagger/issues/174)
- SWAGGER\_SETTINGS permission\_denied\_handler [\#166](https://github.com/marcgibbons/django-rest-swagger/issues/166)

**Merged pull requests:**

- fix smart\_text import \(django-rest-framework 3.x\) [\#175](https://github.com/marcgibbons/django-rest-swagger/pull/175) ([dnozay](https://github.com/dnozay))

## [0.2.5](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.5) (2014-12-11)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.4...0.2.5)

**Closed issues:**

- 'Field' object has no attribute 'default' during introspection. [\#171](https://github.com/marcgibbons/django-rest-swagger/issues/171)
- AssertionError Raised When Using Nested Serializers [\#168](https://github.com/marcgibbons/django-rest-swagger/issues/168)
- Nested Relationships [\#121](https://github.com/marcgibbons/django-rest-swagger/issues/121)
- unable to read api [\#104](https://github.com/marcgibbons/django-rest-swagger/issues/104)

**Merged pull requests:**

- fix \#171 [\#172](https://github.com/marcgibbons/django-rest-swagger/pull/172) ([ariovistus](https://github.com/ariovistus))

## [0.2.4](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.4) (2014-12-10)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.3...0.2.4)

**Closed issues:**

- `\_find\_field\_serializers` Tries to parse drf native serializer - drf v 3 [\#167](https://github.com/marcgibbons/django-rest-swagger/issues/167)

**Merged pull requests:**

- release 0.2.4 [\#170](https://github.com/marcgibbons/django-rest-swagger/pull/170) ([ariovistus](https://github.com/ariovistus))
- fix \#167 [\#169](https://github.com/marcgibbons/django-rest-swagger/pull/169) ([ariovistus](https://github.com/ariovistus))

## [0.2.3](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.3) (2014-12-09)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.2...0.2.3)

**Closed issues:**

- rest\_framework.fields.empty is not JSON serializable [\#163](https://github.com/marcgibbons/django-rest-swagger/issues/163)

**Merged pull requests:**

- release 0.2.3 [\#165](https://github.com/marcgibbons/django-rest-swagger/pull/165) ([ariovistus](https://github.com/ariovistus))
- fix \#163 [\#164](https://github.com/marcgibbons/django-rest-swagger/pull/164) ([ariovistus](https://github.com/ariovistus))

## [0.2.2](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.2) (2014-12-08)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.1...0.2.2)

**Closed issues:**

- fbv failes with Exception: methods \['serializer'\] in class docstring are not in view methods \[u'OPTIONS', u'GET'\] [\#153](https://github.com/marcgibbons/django-rest-swagger/issues/153)

**Merged pull requests:**

- 0.2.2 release [\#162](https://github.com/marcgibbons/django-rest-swagger/pull/162) ([ariovistus](https://github.com/ariovistus))
- preliminary drf3 support [\#161](https://github.com/marcgibbons/django-rest-swagger/pull/161) ([ariovistus](https://github.com/ariovistus))
- Added requirements.txt, setting for doc\_expansion [\#158](https://github.com/marcgibbons/django-rest-swagger/pull/158) ([kaitlin](https://github.com/kaitlin))
- fix \#153 [\#155](https://github.com/marcgibbons/django-rest-swagger/pull/155) ([ariovistus](https://github.com/ariovistus))
- Remove boilerplate code from tox config [\#154](https://github.com/marcgibbons/django-rest-swagger/pull/154) ([maryokhin](https://github.com/maryokhin))
- \#128 plus docs [\#150](https://github.com/marcgibbons/django-rest-swagger/pull/150) ([ariovistus](https://github.com/ariovistus))
- 0.2.1 release [\#149](https://github.com/marcgibbons/django-rest-swagger/pull/149) ([ariovistus](https://github.com/ariovistus))

## [0.2.1](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.1) (2014-11-16)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.2.0...0.2.1)

**Implemented enhancements:**

- Document upcoming YAML parser [\#134](https://github.com/marcgibbons/django-rest-swagger/issues/134)

**Closed issues:**

- Which repo to contribute? [\#146](https://github.com/marcgibbons/django-rest-swagger/issues/146)
- Use YAML to indicate a response serializer other than the default [\#144](https://github.com/marcgibbons/django-rest-swagger/issues/144)
- Add support of choice fields [\#99](https://github.com/marcgibbons/django-rest-swagger/issues/99)
- Custom Parameters for ModelViewSet Methods [\#74](https://github.com/marcgibbons/django-rest-swagger/issues/74)
- custom json render support [\#36](https://github.com/marcgibbons/django-rest-swagger/issues/36)

**Merged pull requests:**

- add a test to \#116 [\#148](https://github.com/marcgibbons/django-rest-swagger/pull/148) ([ariovistus](https://github.com/ariovistus))
- include readthedocs screenshots [\#147](https://github.com/marcgibbons/django-rest-swagger/pull/147) ([ariovistus](https://github.com/ariovistus))
- some initial readthedocs docs [\#145](https://github.com/marcgibbons/django-rest-swagger/pull/145) ([ariovistus](https://github.com/ariovistus))
- suppress those obnoxious colons [\#143](https://github.com/marcgibbons/django-rest-swagger/pull/143) ([ariovistus](https://github.com/ariovistus))
- Preserve the order of fields as declared in serializers [\#140](https://github.com/marcgibbons/django-rest-swagger/pull/140) ([ariovistus](https://github.com/ariovistus))
- yaml different request and response serializers [\#139](https://github.com/marcgibbons/django-rest-swagger/pull/139) ([ariovistus](https://github.com/ariovistus))
- Formatting fixes [\#138](https://github.com/marcgibbons/django-rest-swagger/pull/138) ([dmitry-krasilnikov](https://github.com/dmitry-krasilnikov))
- Unable to read api [\#137](https://github.com/marcgibbons/django-rest-swagger/pull/137) ([peleccom](https://github.com/peleccom))
- Add "info" key to SWAGGER\_SETTINGS [\#136](https://github.com/marcgibbons/django-rest-swagger/pull/136) ([pzrq](https://github.com/pzrq))
- Include nested model serializers recursively [\#116](https://github.com/marcgibbons/django-rest-swagger/pull/116) ([lukas-hetzenecker](https://github.com/lukas-hetzenecker))
- Automatically get JSONRenderer from django rest framework settings [\#87](https://github.com/marcgibbons/django-rest-swagger/pull/87) ([ErwinJunge](https://github.com/ErwinJunge))

## [0.2.0](https://github.com/marcgibbons/django-rest-swagger/tree/0.2.0) (2014-11-01)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.14...0.2.0)

**Closed issues:**

- Fork of django-rest-swagger [\#132](https://github.com/marcgibbons/django-rest-swagger/issues/132)
- RuntimeError after Upgrade to Rest Framework 2.4.3 [\#129](https://github.com/marcgibbons/django-rest-swagger/issues/129)
- Documenting DRF function based views parameters [\#124](https://github.com/marcgibbons/django-rest-swagger/issues/124)
- ViewSetIntrospector broken with DRF 2.4.3 [\#123](https://github.com/marcgibbons/django-rest-swagger/issues/123)
- IS this github repo still ACTIVE? [\#122](https://github.com/marcgibbons/django-rest-swagger/issues/122)
- enabled\_methods not excluding 'put' operations [\#108](https://github.com/marcgibbons/django-rest-swagger/issues/108)
- DocumentationGenerator ignores serializer field order [\#106](https://github.com/marcgibbons/django-rest-swagger/issues/106)
- Error with ternary operation in searching through query strings for ViewSets [\#91](https://github.com/marcgibbons/django-rest-swagger/issues/91)
- Settings are not picked up by swagger \(0.1.14\) [\#78](https://github.com/marcgibbons/django-rest-swagger/issues/78)
- cigar\_example documentation - RuntimeError: Unable to use callback invalid closure/function specified. [\#71](https://github.com/marcgibbons/django-rest-swagger/issues/71)
- Make Python 3 compatible [\#61](https://github.com/marcgibbons/django-rest-swagger/issues/61)

**Merged pull requests:**

- show response statusText [\#135](https://github.com/marcgibbons/django-rest-swagger/pull/135) ([kavardak](https://github.com/kavardak))
- Big honking pull request [\#133](https://github.com/marcgibbons/django-rest-swagger/pull/133) ([ariovistus](https://github.com/ariovistus))

## [0.1.14](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.14) (2014-03-07)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.13...0.1.14)

**Closed issues:**

- How to use exclude\_namespaces  [\#64](https://github.com/marcgibbons/django-rest-swagger/issues/64)

**Merged pull requests:**

- Fixes \#63 missing starting letters from base path in resourses. [\#68](https://github.com/marcgibbons/django-rest-swagger/pull/68) ([bbenko](https://github.com/bbenko))

## [0.1.13](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.13) (2014-02-26)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.12...0.1.13)

**Closed issues:**

- Incomplete resource list [\#63](https://github.com/marcgibbons/django-rest-swagger/issues/63)
- Django Rest Swagger broken on Python 3 due to Unipath bug [\#59](https://github.com/marcgibbons/django-rest-swagger/issues/59)
- unicode SWAGGER\_SETTINGS\['enabled\_methods'\] causes javascript error in python 2 [\#56](https://github.com/marcgibbons/django-rest-swagger/issues/56)
-  CSRF Fails when using 'rest\_framework.authentication.SessionAuthentication' [\#14](https://github.com/marcgibbons/django-rest-swagger/issues/14)

## [0.1.12](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.12) (2014-02-26)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.11...0.1.12)

**Closed issues:**

- http://www.django-rest-framework.org/api-guide/serializers\#serializers [\#55](https://github.com/marcgibbons/django-rest-swagger/issues/55)

**Merged pull requests:**

- Use json serialization of enabled\_methods [\#57](https://github.com/marcgibbons/django-rest-swagger/pull/57) ([davidn](https://github.com/davidn))
- Reworked swagger API Key to work with django-rest-framework's token authentication [\#51](https://github.com/marcgibbons/django-rest-swagger/pull/51) ([DiscoStarslayer](https://github.com/DiscoStarslayer))
- Resolve default values if callable [\#49](https://github.com/marcgibbons/django-rest-swagger/pull/49) ([lukaszb](https://github.com/lukaszb))
- use JSONRendered for SwaggerResourcesView [\#47](https://github.com/marcgibbons/django-rest-swagger/pull/47) ([jfelectron](https://github.com/jfelectron))

## [0.1.11](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.11) (2013-12-01)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.10...0.1.11)

**Closed issues:**

- UnicodeDecodeError: 'ascii' codec can't decode byte 0xe7 in position 22: ordinal not in range\(128\) [\#44](https://github.com/marcgibbons/django-rest-swagger/issues/44)
- Introspector method mapping fails on python \< 2.7 [\#42](https://github.com/marcgibbons/django-rest-swagger/issues/42)
- "settings" object in template is overwritten by contextprocessors that add settings to context [\#40](https://github.com/marcgibbons/django-rest-swagger/issues/40)
- Method-level documentation [\#24](https://github.com/marcgibbons/django-rest-swagger/issues/24)

**Merged pull requests:**

- Add test and fix for not excluding nested URL namespaces [\#41](https://github.com/marcgibbons/django-rest-swagger/pull/41) ([pzrq](https://github.com/pzrq))

## [0.1.10](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.10) (2013-11-24)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.9...0.1.10)

**Closed issues:**

- Viewset support upgrade [\#39](https://github.com/marcgibbons/django-rest-swagger/issues/39)
- Question: How can I specify request-params types from docstring? [\#38](https://github.com/marcgibbons/django-rest-swagger/issues/38)
- Issue when get\_serializer\_class references "self.request" [\#35](https://github.com/marcgibbons/django-rest-swagger/issues/35)
- action and link decoratated methods under a django viewset show all the viewsets HTTP OPTIONS [\#34](https://github.com/marcgibbons/django-rest-swagger/issues/34)
- ImportError: No module named rest\_framework\_swagger [\#33](https://github.com/marcgibbons/django-rest-swagger/issues/33)
- Swagger doesn't inspect all Views [\#31](https://github.com/marcgibbons/django-rest-swagger/issues/31)
- Swagger Specification 1.2 Transition [\#30](https://github.com/marcgibbons/django-rest-swagger/issues/30)
- Question: django-rest-swagger style guide [\#28](https://github.com/marcgibbons/django-rest-swagger/issues/28)
- Unable to find apps [\#21](https://github.com/marcgibbons/django-rest-swagger/issues/21)

## [0.1.9](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.9) (2013-10-01)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.8...0.1.9)

**Closed issues:**

- View description \(notes\) are trimmed. [\#32](https://github.com/marcgibbons/django-rest-swagger/issues/32)
- Support for APPEND\_SLASH = False [\#29](https://github.com/marcgibbons/django-rest-swagger/issues/29)
- django update 1.5.4 - ImportError: No module named core.management [\#25](https://github.com/marcgibbons/django-rest-swagger/issues/25)

## [0.1.8](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.8) (2013-09-16)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.7...0.1.8)

**Closed issues:**

- ImportError: name get\_view\_name [\#22](https://github.com/marcgibbons/django-rest-swagger/issues/22)

**Merged pull requests:**

- Description for serializer fields [\#18](https://github.com/marcgibbons/django-rest-swagger/pull/18) ([lukas-hetzenecker](https://github.com/lukas-hetzenecker))

## [0.1.7](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.7) (2013-09-05)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.6...0.1.7)

**Merged pull requests:**

- fix recursive prefix in \_\_flatten\_patterns\_tree [\#12](https://github.com/marcgibbons/django-rest-swagger/pull/12) ([postfalk](https://github.com/postfalk))
- Added 'api\_path' to settings, it fixes URLs if you don't have API on roo... [\#11](https://github.com/marcgibbons/django-rest-swagger/pull/11) ([whit](https://github.com/whit))

## [0.1.6](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.6) (2013-08-03)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.5...0.1.6)

**Merged pull requests:**

- Relative imports fixes to be compatible with Python 3 [\#10](https://github.com/marcgibbons/django-rest-swagger/pull/10) ([whit](https://github.com/whit))
- Enchancement and bugfix [\#9](https://github.com/marcgibbons/django-rest-swagger/pull/9) ([geraldoandradee](https://github.com/geraldoandradee))

## [0.1.5](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.5) (2013-07-31)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.4...0.1.5)

**Closed issues:**

- Cannot apply DjangoModelPermissions on a view that does not have `.model` or `.queryset` property. [\#8](https://github.com/marcgibbons/django-rest-swagger/issues/8)

## [0.1.4](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.4) (2013-07-29)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.3...0.1.4)

**Closed issues:**

- Missing lib folder in static/rest\_framework\_swagger/ and swagger-ui.js typo? [\#6](https://github.com/marcgibbons/django-rest-swagger/issues/6)
- Installation fails if the Django project root isn't in the PYTHONPATH [\#5](https://github.com/marcgibbons/django-rest-swagger/issues/5)

## [0.1.3](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.3) (2013-07-19)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.2...0.1.3)

**Closed issues:**

- Add support for Routers and ViewSets [\#4](https://github.com/marcgibbons/django-rest-swagger/issues/4)

## [0.1.2](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.2) (2013-07-09)
[Full Changelog](https://github.com/marcgibbons/django-rest-swagger/compare/0.1.1...0.1.2)

## [0.1.1](https://github.com/marcgibbons/django-rest-swagger/tree/0.1.1) (2013-06-28)


\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*