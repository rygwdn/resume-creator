.. role:: right
.. role:: left(strong)
.. role:: sc
.. role:: small


===========
<< name >>
===========

.. list-table::
    :widths: 10 40
    :header-rows: 0
    :class: rststyle-table-personal

    <@ for item in  personal @>
        <@ if not ("pub" in item and not show_personal ) @>
    * -
        .. container:: pers-left

            **<<item.title|rst>>:**

      -
        .. container:: pers-right

            <<item.content|rst>>
        <@ endif @>
    <@endfor@>

Summary
-------

<<summary|rst>>



Work Experience
---------------

.. list-table::
    <# widths are in 1/12th of an inch..
    so do "# cm * (12 / 2.54)" to get value from cm
    total width is 17.27cm
    first col is 2.14cm
    #>
    :widths: <<2.5|cmToTbl>> <<(17.27 - 2.5)|cmToTbl>>
    :header-rows: 0
    :class: rststyle-table-wexp

<@ for item in workexp @>
    <@ set supers = " & ".join(item.superv) @>
    <@ if item.superv|length > 1 @>
        <@ set s = "s" @>
    <@ else @>
        <@ set s = "" @>
    <@ endif @>

    * - .. container:: right

            | <<item.date[0]|rst|indent(4)>>
    <@ if item.date|length > 1 @>
        <@ if item.date[1] == "Current" @>
            | – *<<item.date[1]|rst|indent(8)>>*
        <@ else @>
            | – <<item.date[1]|rst|indent(8)>>
        <@ endif @>
    <@ endif @>

      - .. container:: wexpleft

            .. container:: jobtitle

                <<item.title|rst>>

            .. container:: small

                <@ if item.content @>
                    <<item.content|rst|indent(20)>>
                <@ endif @>

                <@ for bullet in item.content_itemized @>
                    - .. container:: small-bulletitem

                          << bullet|rst|indent(26)>>

                <@ endfor @>

            <@ if type != "pub" @>
            .. container:: right

                `Supervisor<<s>>:`:left: `<<supers>>`:right:
            <@ endif @>

<@ endfor @>



Education
---------

<@ if education.summary -@>
<< education.summary|rst >>
<@ endif @><@ if education.details @>

.. list-table::
   :widths: <<2|cmToTbl>> <<(3)|cmToTbl>> <<(6)|cmToTbl>> <<(17.27 - 10)|cmToTbl>>
   :header-rows: 0
   :class: rststyle-table-nothing

   <@ for item in  education.details @>
   * - .. container:: edu-right

            <<item.date>>:

     - .. container:: shortpar

            <<item.title>>

     - .. container:: edu-center

            :sc:`<<item.institution>>`

     - .. container:: shortpar

             <<item.location>>

   <@ endfor @>
<@- endif @>


Computer Skills
---------------


<@ for item in computer_skills @>
- <<item|rst|indent(2)>>

<@ endfor @>



Awards
------

.. list-table::
    :widths: <<4.26|cmToTbl>> <<(17.27 - 4.26)|cmToTbl>>
    :header-rows: 0
    :class: rststyle-table-nothing

    <@ for item in awards @>
    * -
        .. container:: dateleft

            <<item.date|rst|indent(13)>>

      -
        .. container:: shortpar

            <<item.name|rst|indent(13)>>
    <@ endfor @>


Volunteer Work & Extra Curricular
---------------------------------

<@ for item in volunteer @>
- <<item|rst|indent(2)>>

<@ endfor @>


<@ if type != "pub" @>

<@ if patents @>

Patents
-------

<@ for item in  patents @>
- << item.date|rst>>: << item.name|rst>>, << item.number|rst>>
<@ endfor @>

<@ endif @>

References
----------

.. list-table::
    :widths: <<4.71|cmToTbl>> <<(17.27 - 2*4.71)|cmToTbl>> <<4.71|cmToTbl>>
    :header-rows: 0
    :class: rststyle-table-nothing

    <@ for item in references @>
    * - .. container:: refleft

            <<item.name|rst|indent(13)>>

      - .. container:: refcenter

            :sc:`<<item.job|rst|indent(13)>>`

      - .. container:: refright

            <<item.get("phone", item.get("email", ""))|rst|indent(13)>>

    <@ endfor @>

<@ endif @>
