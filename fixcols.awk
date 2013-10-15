#!/usr/bin/awk

{
    if ($0 ~ /<col .*>/)
    {
        col++;
        printf("<col class=\"col-%d\" />\n", col);
    }
    else
    {
        print $0;
    }

    if ($0 ~ /<colgroup.*>/)
    {
        col = 0;
    }
}
