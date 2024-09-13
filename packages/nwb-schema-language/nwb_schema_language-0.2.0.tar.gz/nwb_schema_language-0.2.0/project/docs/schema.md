
# Class: Schema




URI: [nwb_schema_language:Schema](https://w3id.org/p2p_ld/nwb-schema-language/Schema)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Namespace]++-%20schema_%200..*>[Schema&#124;source:string%20%3F;namespace:string%20%3F;title:string%20%3F;neurodata_types:string%20*;doc:string%20%3F],[Namespace])](https://yuml.me/diagram/nofunky;dir:TB/class/[Namespace]++-%20schema_%200..*>[Schema&#124;source:string%20%3F;namespace:string%20%3F;title:string%20%3F;neurodata_types:string%20*;doc:string%20%3F],[Namespace])

## Referenced by Class

 *  **None** *[➞schema_](schema.md)*  <sub>0..\*</sub>  **[Schema](Schema.md)**

## Attributes


### Own

 * [source](source.md)  <sub>0..1</sub>
     * Description: describes the name of the YAML (or JSON) file with the schema specification. The schema files should be located in the same folder as the namespace file.
     * Range: [String](types/String.md)
 * [namespace](namespace.md)  <sub>0..1</sub>
     * Description: describes a named reference to another namespace. In contrast to source, this is a reference by name to a known namespace (i.e., the namespace is resolved during the build and must point to an already existing namespace). This mechanism is used to allow, e.g., extension of a core namespace (here the NWB core namespace) without requiring hard paths to the files describing the core namespace. Either source or namespace must be specified, but not both.
     * Range: [String](types/String.md)
 * [title](title.md)  <sub>0..1</sub>
     * Description: a descriptive title for a file for documentation purposes.
     * Range: [String](types/String.md)
 * [neurodata_types](neurodata_types.md)  <sub>0..\*</sub>
     * Description: an optional list of strings indicating which data types should be included from the given specification source or namespace. The default is null indicating that all data types should be included.
     * Range: [String](types/String.md)
 * [➞doc](schema__doc.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
