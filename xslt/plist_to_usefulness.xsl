<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
    <xsl:output indent="yes" encoding="UTF-8"/>

    <xsl:template match="/">
        <itms_library>
            <xsl:apply-templates/>
        </itms_library>
    </xsl:template>


    <!-- Processing useless PLIST format -->
    <xsl:template match="/plist/dict/key[string(number(text())) = 'NaN' and text() != 'Tracks']">
        <xsl:variable name="fixed_name" select="lower-case(replace(.,'\s+','_'))"/>
        <xsl:element name="{$fixed_name}">
            <xsl:value-of select="following-sibling::element()[1]/text()"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="/plist/dict/dict/dict">
        <xsl:element name="song">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="/plist/dict/dict/dict/key">
        <xsl:variable name="fixed_name" select="lower-case(replace(.,'\s+','_'))"/>
        <xsl:element name="{$fixed_name}">
            <xsl:value-of select="following-sibling::element()[1]/text()"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="integer|string|data"/>
    
    <xsl:template match="key"/>
    
    <xsl:template match="@*"/>
    

    <!-- process more, this time condense data-->
    <xsl:template match="itms_library">
        <playlist>
            <xsl:apply-templates/>
        </playlist>
    </xsl:template>
    
    <xsl:template match="song">
        <song>
            <xsl:apply-templates/>
        </song>
    </xsl:template>

    <xsl:template match="name|artist|album|genre|play_count|year">
        <xsl:copy-of select="."/>
    </xsl:template>
    
    <xsl:template match="text()"/>
    <xsl:template match="*">
        <xsl:apply-templates/>
    </xsl:template>
</xsl:stylesheet>
