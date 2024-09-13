
# Class: Namespace




URI: [nwb_schema_language:Namespace](https://w3id.org/p2p_ld/nwb-schema-language/Namespace)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Schema],[Schema]<schema_%200..*-++[Namespace&#124;doc:string;name:string;full_name:string%20%3F;version:string;date:datetime%20%3F;author:string%20%2B;contact:string%20%2B],[Namespaces]++-%20namespaces%200..*>[Namespace],[Namespaces])](https://yuml.me/diagram/nofunky;dir:TB/class/[Schema],[Schema]<schema_%200..*-++[Namespace&#124;doc:string;name:string;full_name:string%20%3F;version:string;date:datetime%20%3F;author:string%20%2B;contact:string%20%2B],[Namespaces]++-%20namespaces%200..*>[Namespace],[Namespaces])

## Referenced by Class

 *  **None** *[namespaces](namespaces.md)*  <sub>0..\*</sub>  **[Namespace](Namespace.md)**

## Attributes


### Own

 * [doc](doc.md)  <sub>1..1</sub>
     * Description: Description of corresponding object.
     * Range: [String](types/String.md)
 * [Namespace➞name](Namespace_name.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [full_name](full_name.md)  <sub>0..1</sub>
     * Description: Optional string with extended full name for the namespace.
     * Range: [String](types/String.md)
 * [version](version.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [date](date.md)  <sub>0..1</sub>
     * Description: Date that a namespace was last modified or released
     * Range: [Datetime](types/Datetime.md)
     * Example: 2017-04-25 17:14:13 None
 * [author](author.md)  <sub>1..\*</sub>
     * Description: List of strings with the names of the authors of the namespace.
     * Range: [String](types/String.md)
 * [contact](contact.md)  <sub>1..\*</sub>
     * Description: List of strings with the contact information for the authors. Ordering of the contacts should match the ordering of the authors.
     * Range: [String](types/String.md)
 * [➞schema_](schema.md)  <sub>0..\*</sub>
     * Description: List of the schema to be included in this namespace.
     * Range: [Schema](Schema.md)
