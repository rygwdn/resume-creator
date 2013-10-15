
$rst_init

#filter $clean_rst

.. role:: right
.. role:: left(strong)


===========
$name
===========

.. list-table::
    :widths: 10 40
    :header-rows: 0
    :class: rststyle-table-personal

    #for $item in  $personal
    #if not ($type in $item and not $item.get($type))
    * -
        .. container:: pers-left

            **$item.title:**

      -
        .. container:: pers-right

            $item.content
    #end if
    #end for

Summary
-------

$summary



Education
---------

$education


Work Experience
---------------

.. list-table::
    :widths: 20 100
    :header-rows: 0
    :class: rststyle-table-wexp

#for $item in $workexp
    #set $supers = " & ".join($item.superv)
    #if len($item.superv) > 1
        #set $s = "s"
    #else
        #set $s = ""
    #end if

    #if $item.date[0] == "Current"
    * - *$item.date[0]*
    #else
    * - $item.date[0]
    #end if
    #if len($item.date) > 1
        #if $item.date[1] == "Current"
        - *$item.date[1]*
        #else
        - $item.date[1]
        #end if
    #end if

      - .. container:: wexpleft

            .. container:: jobtitle

                $item.title

            .. container:: small

                $item.content

            #if $type != "pub"
            .. container:: right

                `Supervisor$s:`:left: `$supers`:right:
            #end if

    #if "odtbreak" in $item and $type == "odt"

.. container:: pb

    \ 

.. list-table::
    :widths: 20 100
    :header-rows: 0
    :class: rststyle-table-wexp

    #end if

#end for




Computer Skills
---------------


#for $item in $computer_skills
- $item

#end for



Awards
------

.. list-table::
    :widths: 13 40
    :header-rows: 0
    :class: rststyle-table-nothing

    #for $item in $awards
    #filter $strp_rst
    * -
        .. container:: dateleft

            $item.date

    #end filter
      -
        .. container:: shortpar

            $item.name
    #end for


Volunteer Work & Extra Curricular
---------------------------------

#for $item in $volunteer
- $item

#end for


#if $type != "pub"

References
----------

.. list-table::
    :widths: 9 15 9
    :header-rows: 0
    :class: rststyle-table-nothing

    #for $item in $references
    * - .. container:: refleft

            $item.name

      - .. container:: refcenter

            :sc:`$item.job`

      - .. container:: refright

            $item.phone

    #end for

#end if

#end filter

