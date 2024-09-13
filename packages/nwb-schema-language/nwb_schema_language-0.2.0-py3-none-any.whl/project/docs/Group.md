
# Class: Group




URI: [nwb_schema_language:Group](https://w3id.org/p2p_ld/nwb-schema-language/Group)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Link],[Link]<links%200..*-++[Group&#124;neurodata_type_def:string%20%3F;neurodata_type_inc:string%20%3F;name:string%20%3F;default_name:string%20%3F;doc:string;quantity:string%20%3F;linkable:boolean%20%3F],[Group]<groups%200..*-++[Group],[Dataset]<datasets%200..*-++[Group],[Attribute]<attributes%200..*-++[Group],[Dataset],[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[Link],[Link]<links%200..*-++[Group&#124;neurodata_type_def:string%20%3F;neurodata_type_inc:string%20%3F;name:string%20%3F;default_name:string%20%3F;doc:string;quantity:string%20%3F;linkable:boolean%20%3F],[Group]<groups%200..*-++[Group],[Dataset]<datasets%200..*-++[Group],[Attribute]<attributes%200..*-++[Group],[Dataset],[Attribute])

## Referenced by Class

 *  **None** *[groups](groups.md)*  <sub>0..\*</sub>  **[Group](Group.md)**

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
 * [doc](doc.md)  <sub>1..1</sub>
     * Description: Description of corresponding object.
     * Range: [String](types/String.md)
 * [quantity](quantity.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [linkable](linkable.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
 * [attributes](attributes.md)  <sub>0..\*</sub>
     * Range: [Attribute](Attribute.md)
 * [datasets](datasets.md)  <sub>0..\*</sub>
     * Range: [Dataset](Dataset.md)
 * [groups](groups.md)  <sub>0..\*</sub>
     * Range: [Group](Group.md)
 * [links](links.md)  <sub>0..\*</sub>
     * Range: [Link](Link.md)
