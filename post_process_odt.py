#!/usr/bin/env python
# encoding: utf-8

import ezodf2

def tg(tag):
    tag = tag.split(":")
    return "{%s}%s" % (nsmap[tag[0]], tag[1])

def get_table_row_containing(elem):
    table_row = elem
    table_row_tag = tg("table:table-row")
    while table_row is not None and table_row.tag != table_row_tag:
        table_row = table_row.getparent()

    if table_row is None:
        raise Exception("Failed to find table row containing %r" % elem)
    return table_row

def keep_work_exp_together():
    job_title_p = doc.body.xmlnode.findall(".//text:p[@text:style-name='rststyle-jobtitle']", nsmap)[0]
    table_row = get_table_row_containing(job_title_p)
    table = table_row.getparent()

    style_attrib = tg("table:style-name")
    if style_attrib in table_row.attrib:
        style_name = table_row.attrib[style_attrib]
    else:
        style_name = table.attrib[style_attrib] + ".1"
        for row in table.findall(".//table:table-row", nsmap):
            if style_attrib not in row.attrib:
                row.attrib[style_attrib] = style_name

    print "Adding keep-together:always to work expeirence table (%s)" % style_name
    root_style = doc.content.automatic_styles.xmlnode.makeelement(tg("style:style"), attrib={tg("style:name"): style_name, tg("style:family"): "table-row"}, nsmap=nsmap)
    table_row_properties = root_style.makeelement(tg("style:table-row-properties"), attrib={tg("fo:keep-together"): "always"}, nsmap=nsmap)
    root_style.append(table_row_properties)
    doc.content.automatic_styles.xmlnode.append(root_style)

def keep_table_together(elem):
    table = get_table_row_containing(elem).getparent()
    style_name = table.attrib[tg("table:style-name")]
    style_elem = doc.content.automatic_styles.xmlnode.find(".//style:style[@style:name='%s']" % style_name, nsmap)
    properties = style_elem.find(".//style:table-properties", nsmap)
    print "Adding may-break-between-rows:false to %s" % style_name
    properties.attrib[tg("style:may-break-between-rows")] = "false"

def main():
    global doc, nsmap
    doc = ezodf2.opendoc("out/resume.odt")
    nsmap = doc.body.xmlnode.nsmap

    # work expeirence rows
    keep_work_exp_together()

    # references
    keep_table_together(doc.body.xmlnode.findall(".//text:p[@text:style-name='rststyle-refleft']", nsmap)[0])

    # awards
    keep_table_together(doc.body.xmlnode.findall(".//text:p[@text:style-name='rststyle-dateleft']", nsmap)[0])

    doc.save()

if __name__ == '__main__':
    global doc, nsmap
    main()
