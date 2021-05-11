import lxml.etree as et
import os
from bs4 import BeautifulSoup
import argparse
import glob
from pathlib import Path
from id_image import id_image


def tag_image(path, tags):
    soup = None
    with path.open() as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'xml')
        subject = soup.find("dc:subject")
        if subject is None:
            t = soup.new_tag('dc:subject')
            des = soup.find('rdf:Description')
            des.append(t)
            subject = t
            b = soup.new_tag('rdf:Bag')
            subject.append(b)
            rdf = soup.find("rdf:Description")
            rdf.attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        hsubject = soup.find("lr:hierarchicalSubject")
        if hsubject is None:
            t = soup.new_tag('lr:hierarchicalSubject')
            des = soup.find('rdf:Description')
            des.append(t)
            hsubject = t
            b = soup.new_tag('rdf:Bag')
            hsubject.append(b)
            rdf = soup.find("rdf:Description")
            rdf.attrs['xmlns:lr']="http://ns.adobe.com/lightroom/1.0/"
        tag = soup.new_tag('rdf:li')
        tag.string = 'keras'
        subjectList = subject.find('rdf:Bag')
        subjectList.append( tag)
        hsubjectList = hsubject.find('rdf:Bag')
        for t in tags:
            tagT = soup.new_tag('rdf:li')
            tagT.string = t
            htag = soup.new_tag('rdf:li')
            htag.string = 'keras|' + t
            subjectList.append(tagT)
            hsubjectList.append(htag)    

        # LOAD FROM STRING OR PARSE FROM FILE
    str_xml = str(soup).encode()
    str_xsl = """
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output indent="yes"/>
    <xsl:strip-space elements="*"/>

    <!-- IDENTITY TRANSFORM -->
    <xsl:template match="@*|node()">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:template>

    <!-- RUN normalize-space() ON ALL TEXT NODES -->
    <xsl:template match="text()">
        <xsl:copy-of select="normalize-space()"/>
    </xsl:template>            
</xsl:stylesheet>
"""
        
    doc = et.fromstring(str_xml)
    style = et.fromstring(str_xsl)
    
    # INITIALIZE TRANSFORMER AND RUN 
    transformer = et.XSLT(style)
    result = transformer(doc)
        
    old = path.with_suffix(".old")
    path.replace(old)
    
        # SAVE TO DISK
    with open(os.fspath(path), "w") as out:
        out.write(str(result))
        


def categorize_image(path):
    print ("processing.. " + str(path))
    cats = id_image(str(path)[0:-4])
    tag_image(path, cats)
    
def process_images(patterns):
    for pattern in patterns:
        print(glob.glob(pattern))
        for path in Path(pattern).rglob("*.xmp"):
            categorize_image(path)
    




def main():
    parser = argparse.ArgumentParser(description='Process images')
    parser.add_argument("files", nargs='+')
    args = parser.parse_args()

    process_images(args.files)


    
if __name__ == "__main__":
    main()
