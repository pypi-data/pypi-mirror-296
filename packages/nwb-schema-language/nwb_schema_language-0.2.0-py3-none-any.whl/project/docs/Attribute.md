
# Class: Attribute




URI: [nwb_schema_language:Attribute](https://w3id.org/p2p_ld/nwb-schema-language/Attribute)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[DtypeMixin],[AnyType]<default_value%200..1-++[Attribute&#124;name:string;dims:string%20*;shape:string%20*;doc:string;required:boolean%20%3F;dtype:string%20*],[AnyType]<value%200..1-++[Attribute],[Group]++-%20attributes%200..*>[Attribute],[Dataset]++-%20attributes%200..*>[Attribute],[Attribute]uses%20-.->[DtypeMixin],[Group],[Dataset],[AnyType])](https://yuml.me/diagram/nofunky;dir:TB/class/[DtypeMixin],[AnyType]<default_value%200..1-++[Attribute&#124;name:string;dims:string%20*;shape:string%20*;doc:string;required:boolean%20%3F;dtype:string%20*],[AnyType]<value%200..1-++[Attribute],[Group]++-%20attributes%200..*>[Attribute],[Dataset]++-%20attributes%200..*>[Attribute],[Attribute]uses%20-.->[DtypeMixin],[Group],[Dataset],[AnyType])

## Uses Mixin

 *  mixin: [DtypeMixin](DtypeMixin.md)

## Referenced by Class

 *  **None** *[attributes](attributes.md)*  <sub>0..\*</sub>  **[Attribute](Attribute.md)**

## Attributes


### Own

 * [Attribute➞name](Attribute_name.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [dims](dims.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
 * [shape](shape.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
 * [value](value.md)  <sub>0..1</sub>
     * Description: Optional constant, fixed value for the attribute.
     * Range: [AnyType](AnyType.md)
 * [default_value](default_value.md)  <sub>0..1</sub>
     * Description: Optional default value for variable-valued attributes.
     * Range: [AnyType](AnyType.md)
 * [doc](doc.md)  <sub>1..1</sub>
     * Description: Description of corresponding object.
     * Range: [String](types/String.md)
 * [required](required.md)  <sub>0..1</sub>
     * Description: Optional boolean key describing whether the attribute is required. Default value is True.
     * Range: [Boolean](types/Boolean.md)

### Mixed in from DtypeMixin:

 * [dtype](dtype.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
