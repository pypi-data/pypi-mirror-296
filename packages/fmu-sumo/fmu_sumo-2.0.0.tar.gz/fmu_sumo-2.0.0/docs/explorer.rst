Sumo Explorer
#############

The ``fmu.sumo.explorer`` is a python package for reading data from Sumo in the FMU context.

Note! Access to Sumo is required. For Equinor users, apply through ``AccessIT``.

Installation
-------------

.. code-block:: console

    pip install fmu-sumo

or for the latest development version:

.. code-block:: console

    git clone git@github.com:equinor/fmu-sumo.git
    cd fmu-sumo
    pip install .[dev]

Run tests
---------

.. code-block:: console

    pytest tests/


Api Reference 
-------------

- `API reference <apiref/fmu.sumo.explorer.html>`_

.. warning::
    OpenVDS does not publish builds for MacOS nor for Python version 3.12. You can still use the 
    Explorer without OpenVDS, but some Cube methods will not work.

Usage and examples
------------------

Initializing an Explorer object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We establish a connection to Sumo by initializing an Explorer object.
This object will handle authentication and can be used to retrieve cases and case data.

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer()


Authentication
^^^^^^^^^^^^^^^
If you have not used the `Explorer` before and no access token is found in your system, a login form will open in your web browser.
It is also possible to provide the `Explorer` with an existing token to use for authentication, in this case you will not be prompted to login.

.. code-block:: 

    from fmu.sumo.explorer import Explorer 

    USER_TOKEN="123456789"
    sumo = Explorer(token=USER_TOKEN)

This assumes the `Explorer` is being used within a system which handles authentication and queries Sumo on a users behalf.

Finding a case
^^^^^^^^^^^^^^
The `Explorer` has a property called `cases` which represents all cases you have access to in Sumo:

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    cases = sumo.cases 

The `cases` property is a `CaseCollection` object and acts as a list of cases.
We can use the `filter` method to apply filters to the case collection which will return a new filtered `CaseCollection` instance:

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    cases = sumo.cases
    cases = cases.filter(user="peesv")

In this example we're getting all the cases belonging to user `peesv`.

The resulting `CaseCollection` is iterable:

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    cases = sumo.cases
    cases = cases.filter(user="peesv")

    for case in cases:
        print(case.uuid)
        print(case.name)
        print(case.status)

We can use the filter method to filter on the following properties:

* uuid
* name
* status
* user
* asset
* field

Example: finding all official cases uploaded by `peesv` in Drogon: 

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    cases = sumo.cases
    cases = cases.filter(
        user="peesv",
        status="official",
        asset="Drogon"
    )


The `CaseCollection` has properties which lets us find available filter values.

Example: finding assets 

.. code-block:: 

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    cases = sumo.cases
    cases = cases.filter(
        user="peesv",
        status="official"
    )

    assets = cases.assets

The `CaseCollection.assets` property gives us a list of unique values for the asset property in our list of cases. 
We can now use this information to apply an asset filter:

.. code-block:: 

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    cases = sumo.cases
    cases = cases.filter(
        user="peesv",
        status="official"
    )

    assets = cases.assets

    cases = cases.filter(
        asset=assets[0]
    )

We can retrieve list of unique values for the following properties:

* names 
* statuses
* users 
* assets 
* fields

You can also use a case `uuid` to get a `Case` object:

.. code-block:: 

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    my_case = sumo.get_case_by_uuid("1234567")


Finding cases with specific data types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There is also a filter that searches for cases where there are objects
that match specific criteria. For example, if we define
``4d-seismic`` as objects that have ``data.content=seismic``,
``data.time.t0.label=base`` and ``data.time.t1.label=monitor``, we can use
the ``has`` filter to find cases that have ``4d-seismic`` data:

.. code-block::

   from fmu.sumo.explorer import Explorer, Filters

   exp = Explorer(env="prod")

   cases = exp.cases.filter(asset="Heidrun", has=Filters.seismic4d)

In this case, we have a predefined filter for ``4d-seismic``, exposed
thorugh ``fmu.sumo.explorer.Filters``. There is no magic involved; any
user can create their own filters, and either use them directly or ask
for them to be added to ``fmu.sumo.explorer.Filters``.

It is also possible to chain filters. The previous example could also
be handled by

.. code-block::
   cases = exp.cases.filter(asset="Heidrun",
                            has={"term":{"data.content.keyword": "seismic"}})\
     .filter(has={"term":{"data.time.t0.label.keyword":"base"}})\
     .filter(has={"term":{"data.time.t1.label.keyword":"monitor"}})


Browsing data in a case
^^^^^^^^^^^^^^^^^^^^^^^
The `Case` object has properties for accessing different data types:

* surfaces
* polygons
* tables 

Example: get case surfaces 

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    surfaces = case.surfaces

The `SurfaceCollection` object has a filter method and properties for getting filter values, similar to `CaseCollection`:

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    surfaces = case.surfaces.filter(iteration="iter-0")

    contents = surfaces.contents
    
    surfaces = surfaces.filter(
        content=contents[0]
        )

    names = surfaces.names 

    surfaces = surfaces.filter(
        name=names[0]
    )

    tagnames = surfaces.tagnames 

    surfaces = surfaces.filter(
        tagname=tagnames[0]
    )

    stratigraphic = surfaces.filter(stratigraphic = "false")
    vertical_domain = surfaces.filter(vertical_domain = "depth")


The `SurfaceCollection.filter` method takes the following parameters:

* uuid
* name 
* tagname 
* content 
* dataformat
* iteration 
* realization 
* aggregation
* stage 
* time
* stratigraphic
* vertical_domain

All parameters support a single value, a list of values or a `boolean` value.

Example: get aggregated surfaces 

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    # get mean aggregated surfaces
    surfaces = case.surfaces.filter(aggregation="mean")

    # get min, max and mean aggregated surfaces 
    surfaces = case.surfaces.filter(aggregation=["min", "max", "mean"])

    # get all aggregated surfaces
    surfaces = case.surfaces.filter(aggregation=True)

    # get names of aggregated surfaces 
    names = surfaces.names

We can get list of filter values for the following properties:

* names
* contents 
* tagnames 
* dataformats
* iterations 
* realizations
* aggregations 
* stages 
* timestamps
* intervals
* stratigraphic
* vertical_domain


Once we have a `Surface` object we can get surface metadata using properties:

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    surface = case.surfaces[0]

    print(surface.content)
    print(surface.uuid)
    print(surface.name)
    print(surface.tagname)
    print(surface.dataformat)
    print(surface.stratigraphic)
    print(surface.vertical_domain)

We can get the surface binary data as a `BytesIO` object using the `blob` property. 
The `to_regular_surface` method returns the surface as a `xtgeo.RegularSurface` object.

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    surface = case.surfaces[0]

    # get blob
    blob = surface.blob 

    # get xtgeo.RegularSurface
    reg_surf = surface.to_regular_surface() 

    reg_surf.quickplot()


If we know the `uuid` of the surface we want to work with we can get it directly from the `Explorer` object: 

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    surface = sumo.get_surface_by_uuid("1234567")

    print(surface.name)


Pagination: Iterating over large resultsets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to iterate/paginate over large number of results you _must_ use the 
`keep_alive` parameter to avoid errors and get an exact and complete list of
objects. The `keep_alive` parameter creates a 'snapshot' in the backend, 
which ensures consistent results for you, but at the same time using some
resources on the server-side. To avoid server-side problems, the `keep_alive` 
parameter should be as short as possible, but still large enough for you 
(or your users) to iterate over the data-set. If you are not sure what to 
use, start with 15m, i.e. 15 minutes. This means that you expect that there 
will be a maximum of 15 minutes between each time fmu-sumo calls the back-end, 
so not the complete time period of a user session. 

The 'snapshot' will of course not reflect any updates to data performed 
simultaneously by you or anyone else. 

For how large result-sets should you use the `keep_alive` parameter? As of
early 2024, the `Explorer` uses 500 objects pagination, so you should use 
the `keep_alive` parameter for all result-sets larger than 500 objects. 

The 'snapshot' works in exactly the same way for async and sync methods. 

Here is example code iterating over a large result-set using the `keep_alive` 
parameter:

.. code-block:: python 

    import asyncio

    from fmu.sumo.explorer import Explorer
    from fmu.sumo.explorer.objects import SurfaceCollection

    explorer = Explorer(env="prod", keep_alive="15m")
    case = explorer.get_case_by_uuid("dec73fae-bb11-41f2-be37-73ba005c4967")

    surface_collection: SurfaceCollection = case.surfaces.filter(
        iteration="iter-1",
    )


    async def main():
        count = await surface_collection.length_async()
        for i in range(count):
            print(f"Working on {i} of {count-1}")
            surf = await surface_collection.getitem_async(i)
            # Do something with surf

    asyncio.run(main())

Time filtering
^^^^^^^^^^^^^^
The `TimeFilter` class lets us construct time filters to be used in the `SurfaceCollection.filter` method:

Example: get surfaces with timestamp in a specific range

.. code-block::

    from fmu.sumo.explorer import Explorer, TimeFilter, TimeType

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    time = TimeFilter(
        type=TimeType.TIMESTAMP,
        start="2018-01-01",
        end="2022-01-01"
    )

    surfaces = case.surfaces.filter(time=time)


Example: get surfaces with exact interval 

.. code-block::

    from fmu.sumo.explorer import Explorer, TimeFilter, TimeType

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    time = TimeFilter(
        type=TimeType.INTERVAL,
        start="2018-01-01",
        end="2022-01-01",
        exact=True
    )

    surfaces = case.surfaces.filter(time=time)


Time filters can also be used to get all surfaces that has a specific type of time data.

.. code-block::

    from fmu.sumo.explorer import Explorer, TimeFilter, TimeType

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    # get surfaces with timestamps
    time = TimeFilter(type=TimeType.TIMESTAMP)

    surfaces = case.surfaces.filter(time=time)

    # get surfaces with intervals
    time = TimeFilter(type=TimeType.INTERVAL)

    surfaces = case.surfaces.filter(time=time)

    # get surfaces with any time data
    time = TimeFilter(type=TimeType.ALL)

    surfaces = case.surfaces.filter(time=time)

    # get surfaces without time data
    time = TimeFilter(type=TimeType.NONE)

    surfaces = case.surfaces.filter(time=time)



Performing aggregations
^^^^^^^^^^^^^^^^^^^^^^^
The `SurfaceCollection` class can be used to do on-demand surface aggregations.

.. code-block::

    from fmu.sumo.explorer import Explorer 

    sumo = Explorer() 

    case = sumo.get_case_by_uuid("1234567")

    surfaces = case.surfaces.filter(
        stage="realization",
        content="depth",
        iteration="iter-0",
        name="Valysar Fm.",
        tagname="FACIES_Fraction_Channel"
        stratigraphic="false"
        vertical_domain="depth"
    )

    mean = surfaces.mean()
    min = surfaces.min()
    max = surfaces.max() 
    p10 = surfaces.p10()

    p10.quickplot()

In this example we perform aggregations on all realized instance of the surface `Valysar Fm. (FACIES_Fraction_Channel)` in iteration 0.
The aggregation methods return `xtgeo.RegularSurface` objects.
