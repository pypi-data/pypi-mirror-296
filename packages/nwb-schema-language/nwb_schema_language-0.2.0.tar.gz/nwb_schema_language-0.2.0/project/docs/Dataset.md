
# Class: Dataset




URI: [nwb_schema_language:Dataset](https://w3id.org/p2p_ld/nwb-schema-language/Dataset)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[DtypeMixin],[Attribute]<attributes%200..*-++[Dataset&#124;neurodata_type_def:string%20%3F;neurodata_type_inc:string%20%3F;name:string%20%3F;default_name:string%20%3F;dims:string%20*;shape:string%20*;doc:string;quantity:string%20%3F;linkable:boolean%20%3F;dtype:string%20*],[AnyType]<default_value%200..1-++[Dataset],[AnyType]<value%200..1-++[Dataset],[Group]++-%20datasets%200..*>[Dataset],[Datasets]++-%20datasets%200..*>[Dataset],[Dataset]uses%20-.->[DtypeMixin],[Group],[Datasets],[Attribute],[AnyType])](https://yuml.me/diagram/nofunky;dir:TB/class/[DtypeMixin],[Attribute]<attributes%200..*-++[Dataset&#124;neurodata_type_def:string%20%3F;neurodata_type_inc:string%20%3F;name:string%20%3F;default_name:string%20%3F;dims:string%20*;shape:string%20*;doc:string;quantity:string%20%3F;linkable:boolean%20%3F;dtype:string%20*],[AnyType]<default_value%200..1-++[Dataset],[AnyType]<value%200..1-++[Dataset],[Group]++-%20datasets%200..*>[Dataset],[Datasets]++-%20datasets%200..*>[Dataset],[Dataset]uses%20-.->[DtypeMixin],[Group],[Datasets],[Attribute],[AnyType])

## Uses Mixin

 *  mixin: [DtypeMixin](DtypeMixin.md)

## Referenced by Class

 *  **None** *[datasets](datasets.md)*  <sub>0..\*</sub>  **[Dataset](Dataset.md)**

## Attributes


### Own

 * [neurodata_type_def](neurodata_type_def.md)  <sub>0..1</sub>
     * Description: Used alongside neurodata_type_inc to indicate inheritance, naming, and mixins
     * Range: [String](types/String.md)
 * [neurodata_type_inc](neurodata_type_inc.md)  <sub>0..1</sub>
     * Description: Used alongside neurodata_type_def to indicate inheritance, naming, and mixins
     * Range: [String](types/String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [default_name](default_name.md)  <sub>0..1</sub>
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
 * [quantity](quantity.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [linkable](linkable.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
 * [attributes](attributes.md)  <sub>0..\*</sub>
     * Range: [Attribute](Attribute.md)

### Mixed in from DtypeMixin:

 * [dtype](dtype.md)  <sub>0..\*</sub>
     * Range: [String](types/String.md)
