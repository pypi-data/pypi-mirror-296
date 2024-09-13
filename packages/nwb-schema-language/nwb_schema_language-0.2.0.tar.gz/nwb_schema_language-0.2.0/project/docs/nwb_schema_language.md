
# nwb-schema-language


**metamodel version:** 1.7.0

**version:** None


Translation of the nwb-schema-language to LinkML


### Classes

 * [AnyType](AnyType.md)
 * [Attribute](Attribute.md)
 * [CompoundDtype](CompoundDtype.md)
 * [Dataset](Dataset.md)
 * [Datasets](Datasets.md)
 * [Group](Group.md)
 * [Groups](Groups.md)
 * [Link](Link.md)
 * [Namespace](Namespace.md)
 * [Namespaces](Namespaces.md)
 * [ReferenceDtype](ReferenceDtype.md)
 * [Schema](Schema.md)

### Mixins

 * [DtypeMixin](DtypeMixin.md)

### Slots

 * [attributes](attributes.md)
 * [author](author.md) - List of strings with the names of the authors of the namespace.
 * [contact](contact.md) - List of strings with the contact information for the authors. Ordering of the contacts should match the ordering of the authors.
 * [datasets](datasets.md)
 * [date](date.md) - Date that a namespace was last modified or released
 * [default_name](default_name.md)
 * [default_value](default_value.md) - Optional default value for variable-valued attributes.
 * [dims](dims.md)
 * [doc](doc.md) - Description of corresponding object.
 * [dtype](dtype.md)
     * [CompoundDtype➞dtype](CompoundDtype_dtype.md)
 * [full_name](full_name.md) - Optional string with extended full name for the namespace.
 * [groups](groups.md)
 * [linkable](linkable.md)
 * [links](links.md)
 * [name](name.md)
     * [Attribute➞name](Attribute_name.md)
     * [CompoundDtype➞name](CompoundDtype_name.md)
     * [Namespace➞name](Namespace_name.md)
 * [namespace](namespace.md) - describes a named reference to another namespace. In contrast to source, this is a reference by name to a known namespace (i.e., the namespace is resolved during the build and must point to an already existing namespace). This mechanism is used to allow, e.g., extension of a core namespace (here the NWB core namespace) without requiring hard paths to the files describing the core namespace. Either source or namespace must be specified, but not both.
 * [namespaces](namespaces.md)
 * [neurodata_type_def](neurodata_type_def.md) - Used alongside neurodata_type_inc to indicate inheritance, naming, and mixins
 * [neurodata_type_inc](neurodata_type_inc.md) - Used alongside neurodata_type_def to indicate inheritance, naming, and mixins
 * [neurodata_types](neurodata_types.md) - an optional list of strings indicating which data types should be included from the given specification source or namespace. The default is null indicating that all data types should be included.
 * [quantity](quantity.md)
 * [reftype](reftype.md) - describes the kind of reference
 * [required](required.md) - Optional boolean key describing whether the attribute is required. Default value is True.
 * [➞schema_](schema.md) - List of the schema to be included in this namespace.
 * [➞doc](schema__doc.md)
 * [shape](shape.md)
 * [source](source.md) - describes the name of the YAML (or JSON) file with the schema specification. The schema files should be located in the same folder as the namespace file.
 * [target_type](target_type.md) - Describes the neurodata_type of the target that the reference points to
 * [title](title.md) - a descriptive title for a file for documentation purposes.
 * [value](value.md) - Optional constant, fixed value for the attribute.
 * [version](version.md)

### Enums

 * [FlatDtype](FlatDtype.md)
 * [QuantityEnum](QuantityEnum.md)
 * [reftype_options](reftype_options.md)

### Subsets


### Types


#### Built in

 * **Bool**
 * **Curie**
 * **Decimal**
 * **ElementIdentifier**
 * **NCName**
 * **NodeIdentifier**
 * **URI**
 * **URIorCURIE**
 * **XSDDate**
 * **XSDDateTime**
 * **XSDTime**
 * **float**
 * **int**
 * **str**

#### Defined

 * [Boolean](types/Boolean.md)  (**Bool**)  - A binary (true or false) value
 * [Curie](types/Curie.md)  (**Curie**)  - a compact URI
 * [Date](types/Date.md)  (**XSDDate**)  - a date (year, month and day) in an idealized calendar
 * [DateOrDatetime](types/DateOrDatetime.md)  (**str**)  - Either a date or a datetime
 * [Datetime](types/Datetime.md)  (**XSDDateTime**)  - The combination of a date and time
 * [Decimal](types/Decimal.md)  (**Decimal**)  - A real number with arbitrary precision that conforms to the xsd:decimal specification
 * [Double](types/Double.md)  (**float**)  - A real number that conforms to the xsd:double specification
 * [Float](types/Float.md)  (**float**)  - A real number that conforms to the xsd:float specification
 * [Integer](types/Integer.md)  (**int**)  - An integer
 * [Jsonpath](types/Jsonpath.md)  (**str**)  - A string encoding a JSON Path. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded in tree form.
 * [Jsonpointer](types/Jsonpointer.md)  (**str**)  - A string encoding a JSON Pointer. The value of the string MUST conform to JSON Point syntax and SHOULD dereference to a valid object within the current instance document when encoded in tree form.
 * [Ncname](types/Ncname.md)  (**NCName**)  - Prefix part of CURIE
 * [Nodeidentifier](types/Nodeidentifier.md)  (**NodeIdentifier**)  - A URI, CURIE or BNODE that represents a node in a model.
 * [Objectidentifier](types/Objectidentifier.md)  (**ElementIdentifier**)  - A URI or CURIE that represents an object in the model.
 * [Sparqlpath](types/Sparqlpath.md)  (**str**)  - A string encoding a SPARQL Property Path. The value of the string MUST conform to SPARQL syntax and SHOULD dereference to zero or more valid objects within the current instance document when encoded as RDF.
 * [String](types/String.md)  (**str**)  - A character string
 * [Time](types/Time.md)  (**XSDTime**)  - A time object represents a (local) time of day, independent of any particular day
 * [Uri](types/Uri.md)  (**URI**)  - a complete URI
 * [Uriorcurie](types/Uriorcurie.md)  (**URIorCURIE**)  - a URI or a CURIE
