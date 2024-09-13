
# Class: Link




URI: [nwb_schema_language:Link](https://w3id.org/p2p_ld/nwb-schema-language/Link)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Group]++-%20links%200..*>[Link&#124;name:string%20%3F;doc:string;target_type:string;quantity:string%20%3F],[Group])](https://yuml.me/diagram/nofunky;dir:TB/class/[Group]++-%20links%200..*>[Link&#124;name:string%20%3F;doc:string;target_type:string;quantity:string%20%3F],[Group])

## Referenced by Class

 *  **None** *[links](links.md)*  <sub>0..\*</sub>  **[Link](Link.md)**

## Attributes


### Own

 * [name](name.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [doc](doc.md)  <sub>1..1</sub>
     * Description: Description of corresponding object.
     * Range: [String](types/String.md)
 * [target_type](target_type.md)  <sub>1..1</sub>
     * Description: Describes the neurodata_type of the target that the reference points to
     * Range: [String](types/String.md)
 * [quantity](quantity.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
