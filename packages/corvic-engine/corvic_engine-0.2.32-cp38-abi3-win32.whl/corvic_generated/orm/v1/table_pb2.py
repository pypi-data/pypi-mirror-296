# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: corvic/orm/v1/table.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from corvic_generated.algorithm.graph.v1 import graph_pb2 as corvic_dot_algorithm_dot_graph_dot_v1_dot_graph__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x63orvic/orm/v1/table.proto\x12\rcorvic.orm.v1\x1a\x1b\x62uf/validate/validate.proto\x1a%corvic/algorithm/graph/v1/graph.proto\x1a\x1cgoogle/protobuf/struct.proto\"\xcd\x13\n\x0eTableComputeOp\x12.\n\x05\x65mpty\x18\r \x01(\x0b\x32\x16.corvic.orm.v1.EmptyOpH\x00R\x05\x65mpty\x12T\n\x13select_from_staging\x18\x01 \x01(\x0b\x32\".corvic.orm.v1.SelectFromStagingOpH\x00R\x11selectFromStaging\x12G\n\x0erename_columns\x18\x02 \x01(\x0b\x32\x1e.corvic.orm.v1.RenameColumnsOpH\x00R\rrenameColumns\x12+\n\x04join\x18\x03 \x01(\x0b\x32\x15.corvic.orm.v1.JoinOpH\x00R\x04join\x12G\n\x0eselect_columns\x18\x04 \x01(\x0b\x32\x1e.corvic.orm.v1.SelectColumnsOpH\x00R\rselectColumns\x12;\n\nlimit_rows\x18\x05 \x01(\x0b\x32\x1a.corvic.orm.v1.LimitRowsOpH\x00R\tlimitRows\x12\x35\n\x08order_by\x18\x0f \x01(\x0b\x32\x18.corvic.orm.v1.OrderByOpH\x00R\x07orderBy\x12>\n\x0b\x66ilter_rows\x18\x0b \x01(\x0b\x32\x1b.corvic.orm.v1.FilterRowsOpH\x00R\nfilterRows\x12\x44\n\rdistinct_rows\x18\x0c \x01(\x0b\x32\x1d.corvic.orm.v1.DistinctRowsOpH\x00R\x0c\x64istinctRows\x12J\n\x0fupdate_metadata\x18\x06 \x01(\x0b\x32\x1f.corvic.orm.v1.UpdateMetadataOpH\x00R\x0eupdateMetadata\x12\x41\n\x0cset_metadata\x18\x07 \x01(\x0b\x32\x1c.corvic.orm.v1.SetMetadataOpH\x00R\x0bsetMetadata\x12W\n\x14remove_from_metadata\x18\x08 \x01(\x0b\x32#.corvic.orm.v1.RemoveFromMetadataOpH\x00R\x12removeFromMetadata\x12W\n\x14update_feature_types\x18\t \x01(\x0b\x32#.corvic.orm.v1.UpdateFeatureTypesOpH\x00R\x12updateFeatureTypes\x12Z\n\x15rollup_by_aggregation\x18\n \x01(\x0b\x32$.corvic.orm.v1.RollupByAggregationOpH\x00R\x13rollupByAggregation\x12q\n\x1e\x65mbed_node2vec_from_edge_lists\x18\x0e \x01(\x0b\x32+.corvic.orm.v1.EmbedNode2vecFromEdgeListsOpH\x00R\x1a\x65mbedNode2vecFromEdgeLists\x12P\n\x11\x65mbedding_metrics\x18\x10 \x01(\x0b\x32!.corvic.orm.v1.EmbeddingMetricsOpH\x00R\x10\x65mbeddingMetrics\x12\\\n\x15\x65mbedding_coordinates\x18\x11 \x01(\x0b\x32%.corvic.orm.v1.EmbeddingCoordinatesOpH\x00R\x14\x65mbeddingCoordinates\x12N\n\x11read_from_parquet\x18\x12 \x01(\x0b\x32 .corvic.orm.v1.ReadFromParquetOpH\x00R\x0freadFromParquet\x12g\n\x1aselect_from_vector_staging\x18\x13 \x01(\x0b\x32(.corvic.orm.v1.SelectFromVectorStagingOpH\x00R\x17selectFromVectorStaging\x12\x31\n\x06\x63oncat\x18\x14 \x01(\x0b\x32\x17.corvic.orm.v1.ConcatOpH\x00R\x06\x63oncat\x12\x44\n\runnest_struct\x18\x15 \x01(\x0b\x32\x1d.corvic.orm.v1.UnnestStructOpH\x00R\x0cunnestStruct\x12K\n\x10nest_into_struct\x18\x19 \x01(\x0b\x32\x1f.corvic.orm.v1.NestIntoStructOpH\x00R\x0enestIntoStruct\x12Q\n\x12\x61\x64\x64_literal_column\x18\x16 \x01(\x0b\x32!.corvic.orm.v1.AddLiteralColumnOpH\x00R\x10\x61\x64\x64LiteralColumn\x12J\n\x0f\x63ombine_columns\x18\x17 \x01(\x0b\x32\x1f.corvic.orm.v1.CombineColumnsOpH\x00R\x0e\x63ombineColumns\x12\x41\n\x0c\x65mbed_column\x18\x18 \x01(\x0b\x32\x1c.corvic.orm.v1.EmbedColumnOpH\x00R\x0b\x65mbedColumn\x12\x44\n\rencode_column\x18\x1a \x01(\x0b\x32\x1d.corvic.orm.v1.EncodeColumnOpH\x00R\x0c\x65ncodeColumn\x12P\n\x11\x61ggregate_columns\x18\x1b \x01(\x0b\x32!.corvic.orm.v1.AggregateColumnsOpH\x00R\x10\x61ggregateColumns\x12P\n\x11\x63orrelate_columns\x18\x1c \x01(\x0b\x32!.corvic.orm.v1.CorrelateColumnsOpH\x00R\x10\x63orrelateColumns\x12M\n\x10histogram_column\x18\x1d \x01(\x0b\x32 .corvic.orm.v1.HistogramColumnOpH\x00R\x0fhistogramColumn\x12\\\n\x15\x63onvert_column_string\x18\x1e \x01(\x0b\x32&.corvic.orm.v1.ConvertColumnToStringOpH\x00R\x13\x63onvertColumnString\x12;\n\trow_index\x18\x1f \x01(\x0b\x32\x1c.corvic.orm.v1.AddRowIndexOpH\x00R\x08rowIndex\x12;\n\noutput_csv\x18  \x01(\x0b\x32\x1a.corvic.orm.v1.OutputCsvOpH\x00R\toutputCsv\x12\x44\n\rtruncate_list\x18! \x01(\x0b\x32\x1d.corvic.orm.v1.TruncateListOpH\x00R\x0ctruncateListB\x04\n\x02op\"\x8f\x02\n\x06JoinOp\x12>\n\x0bleft_source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\nleftSource\x12*\n\x11left_join_columns\x18\x02 \x03(\tR\x0fleftJoinColumns\x12@\n\x0cright_source\x18\x03 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x0brightSource\x12,\n\x12right_join_columns\x18\x04 \x03(\tR\x10rightJoinColumns\x12)\n\x03how\x18\x05 \x01(\x0e\x32\x17.corvic.orm.v1.JoinTypeR\x03how\"\xe6\x01\n\x0fRenameColumnsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12Z\n\x10old_names_to_new\x18\x02 \x03(\x0b\x32\x31.corvic.orm.v1.RenameColumnsOp.OldNamesToNewEntryR\roldNamesToNew\x1a@\n\x12OldNamesToNewEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\x11\n\x0fTextFeatureType\"\x18\n\x16\x43\x61tegoricalFeatureType\"\x17\n\x15PrimaryKeyFeatureType\"I\n\x15\x46oreignKeyFeatureType\x12\x30\n\x14referenced_source_id\x18\x01 \x01(\tR\x12referencedSourceId\"\x17\n\x15IdentifierFeatureType\"\x16\n\x14NumericalFeatureType\"\x1d\n\x1bMultiCategoricalFeatureType\"\x16\n\x14TimestampFeatureType\"\x16\n\x14\x45mbeddingFeatureType\"\x14\n\x12UnknownFeatureType\"\xfd\x05\n\x0b\x46\x65\x61tureType\x12\x34\n\x04text\x18\x01 \x01(\x0b\x32\x1e.corvic.orm.v1.TextFeatureTypeH\x00R\x04text\x12I\n\x0b\x63\x61tegorical\x18\x02 \x01(\x0b\x32%.corvic.orm.v1.CategoricalFeatureTypeH\x00R\x0b\x63\x61tegorical\x12G\n\x0bprimary_key\x18\x03 \x01(\x0b\x32$.corvic.orm.v1.PrimaryKeyFeatureTypeH\x00R\nprimaryKey\x12G\n\x0b\x66oreign_key\x18\x04 \x01(\x0b\x32$.corvic.orm.v1.ForeignKeyFeatureTypeH\x00R\nforeignKey\x12\x46\n\nidentifier\x18\x05 \x01(\x0b\x32$.corvic.orm.v1.IdentifierFeatureTypeH\x00R\nidentifier\x12\x43\n\tnumerical\x18\x06 \x01(\x0b\x32#.corvic.orm.v1.NumericalFeatureTypeH\x00R\tnumerical\x12Y\n\x11multi_categorical\x18\x07 \x01(\x0b\x32*.corvic.orm.v1.MultiCategoricalFeatureTypeH\x00R\x10multiCategorical\x12\x43\n\ttimestamp\x18\x08 \x01(\x0b\x32#.corvic.orm.v1.TimestampFeatureTypeH\x00R\ttimestamp\x12\x43\n\tembedding\x18\t \x01(\x0b\x32#.corvic.orm.v1.EmbeddingFeatureTypeH\x00R\tembedding\x12=\n\x07unknown\x18\n \x01(\x0b\x32!.corvic.orm.v1.UnknownFeatureTypeH\x00R\x07unknown\x12\x1f\n\x0bis_excluded\x18\x0b \x01(\x08R\nisExcludedB\t\n\x07\x66\x65\x61ture\"\xcc\x01\n\x13SelectFromStagingOp\x12\x1d\n\nblob_names\x18\x01 \x03(\tR\tblobNames\x12#\n\rexpected_rows\x18\x03 \x01(\x04R\x0c\x65xpectedRows\x12!\n\x0c\x61rrow_schema\x18\x04 \x01(\x0cR\x0b\x61rrowSchema\x12?\n\rfeature_types\x18\x05 \x03(\x0b\x32\x1a.corvic.orm.v1.FeatureTypeR\x0c\x66\x65\x61tureTypesJ\x04\x08\x02\x10\x03R\x07\x63olumns\"b\n\x0fSelectColumnsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x18\n\x07\x63olumns\x18\x02 \x03(\tR\x07\x63olumns\"_\n\x0bLimitRowsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x19\n\x08num_rows\x18\x02 \x01(\x04R\x07numRows\"p\n\tOrderByOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x18\n\x07\x63olumns\x18\x02 \x03(\tR\x07\x63olumns\x12\x12\n\x04\x64\x65sc\x18\x03 \x01(\x08R\x04\x64\x65sc\"~\n\x0c\x46ilterRowsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x37\n\nrow_filter\x18\x02 \x01(\x0b\x32\x18.corvic.orm.v1.RowFilterR\trowFilter\"G\n\x0e\x44istinctRowsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\"\x8d\x01\n\x10UpdateMetadataOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x42\n\x10metadata_updates\x18\x02 \x01(\x0b\x32\x17.google.protobuf.StructR\x0fmetadataUpdates\"\x82\x01\n\rSetMetadataOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12:\n\x0cnew_metadata\x18\x02 \x01(\x0b\x32\x17.google.protobuf.StructR\x0bnewMetadata\"s\n\x14RemoveFromMetadataOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12$\n\x0ekeys_to_remove\x18\x02 \x03(\tR\x0ckeysToRemove\"\x93\x02\n\x14UpdateFeatureTypesOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x64\n\x11new_feature_types\x18\x02 \x03(\x0b\x32\x38.corvic.orm.v1.UpdateFeatureTypesOp.NewFeatureTypesEntryR\x0fnewFeatureTypes\x1a^\n\x14NewFeatureTypesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32\x1a.corvic.orm.v1.FeatureTypeR\x05value:\x02\x38\x01\"\xfa\x01\n\x15RollupByAggregationOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x31\n\x15group_by_column_names\x18\x02 \x03(\tR\x12groupByColumnNames\x12,\n\x12target_column_name\x18\x03 \x01(\tR\x10targetColumnName\x12I\n\x10\x61ggregation_type\x18\x04 \x01(\x0e\x32\x1e.corvic.orm.v1.AggregationTypeR\x0f\x61ggregationType\"\xa8\x01\n\x17\x43ombineFiltersRowFilter\x12\x39\n\x0brow_filters\x18\x01 \x03(\x0b\x32\x18.corvic.orm.v1.RowFilterR\nrowFilters\x12R\n\x13logical_combination\x18\x02 \x01(\x0e\x32!.corvic.orm.v1.LogicalCombinationR\x12logicalCombination\"\xbc\x01\n\x1f\x43ompareColumnToLiteralRowFilter\x12\x1f\n\x0b\x63olumn_name\x18\x01 \x01(\tR\ncolumnName\x12\x30\n\x07literal\x18\x02 \x01(\x0b\x32\x16.google.protobuf.ValueR\x07literal\x12\x46\n\x0f\x63omparison_type\x18\x03 \x01(\x0e\x32\x1d.corvic.orm.v1.ComparisonTypeR\x0e\x63omparisonType\"\xd5\x01\n\tRowFilter\x12k\n\x19\x63ompare_column_to_literal\x18\x01 \x01(\x0b\x32..corvic.orm.v1.CompareColumnToLiteralRowFilterH\x00R\x16\x63ompareColumnToLiteral\x12Q\n\x0f\x63ombine_filters\x18\x02 \x01(\x0b\x32&.corvic.orm.v1.CombineFiltersRowFilterH\x00R\x0e\x63ombineFiltersB\x08\n\x06\x66ilter\"\t\n\x07\x45mptyOp\"\xec\x01\n\rEdgeListTable\x12\x33\n\x05table\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x05table\x12*\n\x11start_column_name\x18\x02 \x01(\tR\x0fstartColumnName\x12&\n\x0f\x65nd_column_name\x18\x03 \x01(\tR\rendColumnName\x12*\n\x11start_entity_name\x18\x04 \x01(\tR\x0fstartEntityName\x12&\n\x0f\x65nd_entity_name\x18\x05 \x01(\tR\rendEntityName\"\xc6\x01\n\x1c\x45mbedNode2vecFromEdgeListsOp\x12\x46\n\x10\x65\x64ge_list_tables\x18\x01 \x03(\x0b\x32\x1c.corvic.orm.v1.EdgeListTableR\x0e\x65\x64geListTables\x12^\n\x13node2vec_parameters\x18\x02 \x01(\x0b\x32-.corvic.algorithm.graph.v1.Node2VecParametersR\x12node2vecParameters\"}\n\x12\x45mbeddingMetricsOp\x12\x33\n\x05table\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x05table\x12\x32\n\x15\x65mbedding_column_name\x18\x02 \x01(\tR\x13\x65mbeddingColumnName\"\xd6\x01\n\x16\x45mbeddingCoordinatesOp\x12\x33\n\x05table\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x05table\x12!\n\x0cn_components\x18\x02 \x01(\x04R\x0bnComponents\x12\x30\n\x06metric\x18\x03 \x01(\tB\x18\xbaH\x15r\x13R\teuclideanR\x06\x63osineR\x06metric\x12\x32\n\x15\x65mbedding_column_name\x18\x04 \x01(\tR\x13\x65mbeddingColumnName\"\xbb\x01\n\x11ReadFromParquetOp\x12\x1d\n\nblob_names\x18\x01 \x03(\tR\tblobNames\x12#\n\rexpected_rows\x18\x02 \x01(\x04R\x0c\x65xpectedRows\x12!\n\x0c\x61rrow_schema\x18\x03 \x01(\x0cR\x0b\x61rrowSchema\x12?\n\rfeature_types\x18\x04 \x03(\x0b\x32\x1a.corvic.orm.v1.FeatureTypeR\x0c\x66\x65\x61tureTypes\"\xee\x02\n\x19SelectFromVectorStagingOp\x12!\n\x0cinput_vector\x18\x01 \x03(\x02R\x0binputVector\x12\x1d\n\nblob_names\x18\x02 \x03(\tR\tblobNames\x12\x45\n\x11similarity_metric\x18\x03 \x01(\tB\x18\xbaH\x15r\x13R\teuclideanR\x06\x63osineR\x10similarityMetric\x12,\n\x12vector_column_name\x18\x04 \x01(\tR\x10vectorColumnName\x12!\n\x0c\x61rrow_schema\x18\x06 \x01(\x0cR\x0b\x61rrowSchema\x12?\n\rfeature_types\x18\x07 \x03(\x0b\x32\x1a.corvic.orm.v1.FeatureTypeR\x0c\x66\x65\x61tureTypes\x12#\n\rexpected_rows\x18\x08 \x01(\x04R\x0c\x65xpectedRowsJ\x04\x08\x05\x10\x06R\x0bnum_results\"\xa8\x01\n\x08\x43oncatOp\x12\x35\n\x06tables\x18\x01 \x03(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06tables\x12\x65\n\x03how\x18\x02 \x01(\tBS\xbaHPrKR\x08verticalR\x10vertical_relaxedR\x08\x64iagonalR\x10\x64iagonal_relaxedR\nhorizontalR\x05\x61lign\xd0\x01\x01R\x03how\"u\n\x0eUnnestStructOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12,\n\x12struct_column_name\x18\x02 \x01(\tR\x10structColumnName\"\xa8\x01\n\x10NestIntoStructOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12,\n\x12struct_column_name\x18\x02 \x01(\tR\x10structColumnName\x12/\n\x14\x63olumn_names_to_nest\x18\x03 \x03(\tR\x11\x63olumnNamesToNest\"\xb1\x02\n\x12\x41\x64\x64LiteralColumnOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x34\n\x07literal\x18\x02 \x01(\x0b\x32\x16.google.protobuf.ValueB\x02\x18\x01R\x07literal\x12\x32\n\x08literals\x18\x05 \x03(\x0b\x32\x16.google.protobuf.ValueR\x08literals\x12.\n\x13\x63olumn_arrow_schema\x18\x03 \x01(\x0cR\x11\x63olumnArrowSchema\x12J\n\x13\x63olumn_feature_type\x18\x04 \x01(\x0b\x32\x1a.corvic.orm.v1.FeatureTypeR\x11\x63olumnFeatureType\",\n\x0c\x43oncatString\x12\x1c\n\tseparator\x18\x01 \x01(\tR\tseparator\"\x0c\n\nConcatList\"\xad\x02\n\x10\x43ombineColumnsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12!\n\x0c\x63olumn_names\x18\x02 \x03(\tR\x0b\x63olumnNames\x12\x30\n\x14\x63ombined_column_name\x18\x03 \x01(\tR\x12\x63ombinedColumnName\x12\x42\n\rconcat_string\x18\x04 \x01(\x0b\x32\x1b.corvic.orm.v1.ConcatStringH\x00R\x0c\x63oncatString\x12<\n\x0b\x63oncat_list\x18\x05 \x01(\x0b\x32\x19.corvic.orm.v1.ConcatListH\x00R\nconcatListB\x0b\n\treduction\"\x0f\n\rOneHotEncoder\"f\n\x0cMinMaxScaler\x12*\n\x11\x66\x65\x61ture_range_min\x18\x01 \x01(\x03R\x0f\x66\x65\x61tureRangeMin\x12*\n\x11\x66\x65\x61ture_range_max\x18\x02 \x01(\x03R\x0f\x66\x65\x61tureRangeMax\"J\n\x0eLabelBinarizer\x12\x1b\n\tneg_label\x18\x01 \x01(\x03R\x08negLabel\x12\x1b\n\tpos_label\x18\x02 \x01(\x03R\x08posLabel\"\x0e\n\x0cLabelEncoder\"\xa5\x01\n\x10KBinsDiscretizer\x12\x1e\n\x06n_bins\x18\x01 \x01(\x04\x42\x07\xbaH\x04\x32\x02(\x02R\x05nBins\x12\x33\n\rencode_method\x18\x02 \x01(\tB\x0e\xbaH\x0br\tR\x07ordinalR\x0c\x65ncodeMethod\x12<\n\x08strategy\x18\x03 \x01(\tB \xbaH\x1dr\x1bR\x07uniformR\x08quantileR\x06kmeansR\x08strategy\")\n\tBinarizer\x12\x1c\n\tthreshold\x18\x01 \x01(\x02R\tthreshold\"\x0e\n\x0cMaxAbsScaler\"H\n\x0eStandardScaler\x12\x1b\n\twith_mean\x18\x01 \x01(\x08R\x08withMean\x12\x19\n\x08with_std\x18\x02 \x01(\x08R\x07withStd\"\xc9\x04\n\x07\x45ncoder\x12\x46\n\x0fone_hot_encoder\x18\x01 \x01(\x0b\x32\x1c.corvic.orm.v1.OneHotEncoderH\x00R\roneHotEncoder\x12\x43\n\x0emin_max_scaler\x18\x02 \x01(\x0b\x32\x1b.corvic.orm.v1.MinMaxScalerH\x00R\x0cminMaxScaler\x12H\n\x0flabel_binarizer\x18\x03 \x01(\x0b\x32\x1d.corvic.orm.v1.LabelBinarizerH\x00R\x0elabelBinarizer\x12\x42\n\rlabel_encoder\x18\x04 \x01(\x0b\x32\x1b.corvic.orm.v1.LabelEncoderH\x00R\x0clabelEncoder\x12O\n\x12k_bins_discretizer\x18\x05 \x01(\x0b\x32\x1f.corvic.orm.v1.KBinsDiscretizerH\x00R\x10kBinsDiscretizer\x12\x38\n\tbinarizer\x18\x06 \x01(\x0b\x32\x18.corvic.orm.v1.BinarizerH\x00R\tbinarizer\x12\x43\n\x0emax_abs_scaler\x18\x07 \x01(\x0b\x32\x1b.corvic.orm.v1.MaxAbsScalerH\x00R\x0cmaxAbsScaler\x12H\n\x0fstandard_scaler\x18\x08 \x01(\x0b\x32\x1d.corvic.orm.v1.StandardScalerH\x00R\x0estandardScalerB\t\n\x07\x65ncoder\"\xca\x01\n\x0e\x45ncodeColumnOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x1f\n\x0b\x63olumn_name\x18\x02 \x01(\tR\ncolumnName\x12.\n\x13\x65ncoded_column_name\x18\x03 \x01(\tR\x11\x65ncodedColumnName\x12\x30\n\x07\x65ncoder\x18\x04 \x01(\x0b\x32\x16.corvic.orm.v1.EncoderR\x07\x65ncoder\"\xf7\x02\n\rEmbedColumnOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x1f\n\x0b\x63olumn_name\x18\x02 \x01(\tR\ncolumnName\x12\x32\n\x15\x65mbedding_column_name\x18\x03 \x01(\tR\x13\x65mbeddingColumnName\x12\x1d\n\nmodel_name\x18\x04 \x01(\tR\tmodelName\x12%\n\x0etokenizer_name\x18\x05 \x01(\tR\rtokenizerName\x12\x34\n\x16\x65xpected_vector_length\x18\x06 \x01(\rR\x14\x65xpectedVectorLength\x12^\n\x1c\x65xpected_coordinate_bitwidth\x18\x07 \x01(\x0e\x32\x1c.corvic.orm.v1.FloatBitWidthR\x1a\x65xpectedCoordinateBitwidth\"\x05\n\x03Min\"\x05\n\x03Max\"\x06\n\x04Mean\"\x05\n\x03Std\"&\n\x08Quantile\x12\x1a\n\x08quantile\x18\x01 \x01(\x02R\x08quantile\"\x07\n\x05\x43ount\"\x0b\n\tNullCount\"\xdf\x02\n\x0b\x41ggregation\x12&\n\x03min\x18\x01 \x01(\x0b\x32\x12.corvic.orm.v1.MinH\x00R\x03min\x12&\n\x03max\x18\x02 \x01(\x0b\x32\x12.corvic.orm.v1.MaxH\x00R\x03max\x12)\n\x04mean\x18\x03 \x01(\x0b\x32\x13.corvic.orm.v1.MeanH\x00R\x04mean\x12&\n\x03std\x18\x04 \x01(\x0b\x32\x12.corvic.orm.v1.StdH\x00R\x03std\x12\x35\n\x08quantile\x18\x05 \x01(\x0b\x32\x17.corvic.orm.v1.QuantileH\x00R\x08quantile\x12,\n\x05\x63ount\x18\x06 \x01(\x0b\x32\x14.corvic.orm.v1.CountH\x00R\x05\x63ount\x12\x39\n\nnull_count\x18\x07 \x01(\x0b\x32\x18.corvic.orm.v1.NullCountH\x00R\tnullCountB\r\n\x0b\x61ggregation\"\xac\x01\n\x12\x41ggregateColumnsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12!\n\x0c\x63olumn_names\x18\x02 \x03(\tR\x0b\x63olumnNames\x12<\n\x0b\x61ggregation\x18\x03 \x01(\x0b\x32\x1a.corvic.orm.v1.AggregationR\x0b\x61ggregation\"n\n\x12\x43orrelateColumnsOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12!\n\x0c\x63olumn_names\x18\x02 \x03(\tR\x0b\x63olumnNames\"\xcd\x01\n\x11HistogramColumnOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x1f\n\x0b\x63olumn_name\x18\x02 \x01(\tR\ncolumnName\x12\x34\n\x16\x62reakpoint_column_name\x18\x03 \x01(\tR\x14\x62reakpointColumnName\x12*\n\x11\x63ount_column_name\x18\x04 \x01(\tR\x0f\x63ountColumnName\"\x91\x01\n\rAddRowIndexOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x31\n\x15row_index_column_name\x18\x02 \x01(\tR\x12rowIndexColumnName\x12\x16\n\x06offset\x18\x03 \x01(\x04R\x06offset\"q\n\x17\x43onvertColumnToStringOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x1f\n\x0b\x63olumn_name\x18\x02 \x01(\tR\ncolumnName\"\x84\x01\n\x0bOutputCsvOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12\x17\n\x07\x63sv_url\x18\x02 \x01(\tR\x06\x63svUrl\x12%\n\x0einclude_header\x18\x03 \x01(\x08R\rincludeHeader\"\xe0\x01\n\x0eTruncateListOp\x12\x35\n\x06source\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x06source\x12(\n\x10list_column_name\x18\x02 \x01(\tR\x0elistColumnName\x12\x30\n\x14target_column_length\x18\x03 \x01(\rR\x12targetColumnLength\x12;\n\rpadding_value\x18\x04 \x01(\x0b\x32\x16.google.protobuf.ValueR\x0cpaddingValue\"@\n\x0eTableSliceArgs\x12\x16\n\x06offset\x18\x01 \x01(\x04R\x06offset\x12\x16\n\x06length\x18\x02 \x01(\x04R\x06length\"\xe7\x01\n\x13TableComputeContext\x12\x33\n\x05table\x18\x01 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x05table\x12*\n\x11output_url_prefix\x18\x02 \x01(\tR\x0foutputUrlPrefix\x12U\n\x15sql_output_slice_args\x18\x03 \x01(\x0b\x32\x1d.corvic.orm.v1.TableSliceArgsH\x00R\x12sqlOutputSliceArgs\x88\x01\x01\x42\x18\n\x16_sql_output_slice_args\"h\n\x12TableComputeResult\x12\x1f\n\x0bresult_urls\x18\x02 \x03(\tR\nresultUrls\x12\x31\n\x07metrics\x18\x01 \x01(\x0b\x32\x17.google.protobuf.StructR\x07metrics\"\x86\x01\n\x0e\x45xecuteRequest\x12N\n\x11tables_to_compute\x18\x03 \x03(\x0b\x32\".corvic.orm.v1.TableComputeContextR\x0ftablesToComputeJ\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03R\x05tableR\x11output_url_prefix\"l\n\x0f\x45xecuteResponse\x12\x46\n\rtable_results\x18\x01 \x03(\x0b\x32!.corvic.orm.v1.TableComputeResultR\x0ctableResultsJ\x04\x08\x02\x10\x03R\x0boutput_urls\"d\n\x14StreamExecuteRequest\x12L\n\x10table_to_compute\x18\x01 \x01(\x0b\x32\".corvic.orm.v1.TableComputeContextR\x0etableToCompute\"_\n\x15StreamExecuteResponse\x12\x46\n\rtable_results\x18\x01 \x03(\x0b\x32!.corvic.orm.v1.TableComputeResultR\x0ctableResults\"\xa7\x01\n\x0bNamedTables\x12>\n\x06tables\x18\x01 \x03(\x0b\x32&.corvic.orm.v1.NamedTables.TablesEntryR\x06tables\x1aX\n\x0bTablesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x33\n\x05value\x18\x02 \x01(\x0b\x32\x1d.corvic.orm.v1.TableComputeOpR\x05value:\x02\x38\x01*T\n\x08JoinType\x12\x19\n\x15JOIN_TYPE_UNSPECIFIED\x10\x00\x12\x13\n\x0fJOIN_TYPE_INNER\x10\x01\x12\x18\n\x14JOIN_TYPE_LEFT_OUTER\x10\x02*\xd2\x01\n\x0f\x41ggregationType\x12 \n\x1c\x41GGREGATION_TYPE_UNSPECIFIED\x10\x00\x12\x1a\n\x16\x41GGREGATION_TYPE_COUNT\x10\x01\x12\x18\n\x14\x41GGREGATION_TYPE_AVG\x10\x02\x12\x19\n\x15\x41GGREGATION_TYPE_MODE\x10\x03\x12\x18\n\x14\x41GGREGATION_TYPE_MIN\x10\x04\x12\x18\n\x14\x41GGREGATION_TYPE_MAX\x10\x05\x12\x18\n\x14\x41GGREGATION_TYPE_SUM\x10\x06*s\n\x12LogicalCombination\x12#\n\x1fLOGICAL_COMBINATION_UNSPECIFIED\x10\x00\x12\x1b\n\x17LOGICAL_COMBINATION_ANY\x10\x01\x12\x1b\n\x17LOGICAL_COMBINATION_ALL\x10\x02*\xc1\x01\n\x0e\x43omparisonType\x12\x1f\n\x1b\x43OMPARISON_TYPE_UNSPECIFIED\x10\x00\x12\x16\n\x12\x43OMPARISON_TYPE_EQ\x10\x01\x12\x16\n\x12\x43OMPARISON_TYPE_NE\x10\x02\x12\x16\n\x12\x43OMPARISON_TYPE_LT\x10\x03\x12\x16\n\x12\x43OMPARISON_TYPE_GT\x10\x04\x12\x16\n\x12\x43OMPARISON_TYPE_LE\x10\x05\x12\x16\n\x12\x43OMPARISON_TYPE_GE\x10\x06*`\n\rFloatBitWidth\x12\x1f\n\x1b\x46LOAT_BIT_WIDTH_UNSPECIFIED\x10\x00\x12\x16\n\x12\x46LOAT_BIT_WIDTH_32\x10\x01\x12\x16\n\x12\x46LOAT_BIT_WIDTH_64\x10\x02\x32\xc1\x01\n\x13TableComputeService\x12J\n\x07\x45xecute\x12\x1d.corvic.orm.v1.ExecuteRequest\x1a\x1e.corvic.orm.v1.ExecuteResponse\"\x00\x12^\n\rStreamExecute\x12#.corvic.orm.v1.StreamExecuteRequest\x1a$.corvic.orm.v1.StreamExecuteResponse\"\x00(\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'corvic.orm.v1.table_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RENAMECOLUMNSOP_OLDNAMESTONEWENTRY']._options = None
  _globals['_RENAMECOLUMNSOP_OLDNAMESTONEWENTRY']._serialized_options = b'8\001'
  _globals['_UPDATEFEATURETYPESOP_NEWFEATURETYPESENTRY']._options = None
  _globals['_UPDATEFEATURETYPESOP_NEWFEATURETYPESENTRY']._serialized_options = b'8\001'
  _globals['_EMBEDDINGCOORDINATESOP'].fields_by_name['metric']._options = None
  _globals['_EMBEDDINGCOORDINATESOP'].fields_by_name['metric']._serialized_options = b'\272H\025r\023R\teuclideanR\006cosine'
  _globals['_SELECTFROMVECTORSTAGINGOP'].fields_by_name['similarity_metric']._options = None
  _globals['_SELECTFROMVECTORSTAGINGOP'].fields_by_name['similarity_metric']._serialized_options = b'\272H\025r\023R\teuclideanR\006cosine'
  _globals['_CONCATOP'].fields_by_name['how']._options = None
  _globals['_CONCATOP'].fields_by_name['how']._serialized_options = b'\272HPrKR\010verticalR\020vertical_relaxedR\010diagonalR\020diagonal_relaxedR\nhorizontalR\005align\320\001\001'
  _globals['_ADDLITERALCOLUMNOP'].fields_by_name['literal']._options = None
  _globals['_ADDLITERALCOLUMNOP'].fields_by_name['literal']._serialized_options = b'\030\001'
  _globals['_KBINSDISCRETIZER'].fields_by_name['n_bins']._options = None
  _globals['_KBINSDISCRETIZER'].fields_by_name['n_bins']._serialized_options = b'\272H\0042\002(\002'
  _globals['_KBINSDISCRETIZER'].fields_by_name['encode_method']._options = None
  _globals['_KBINSDISCRETIZER'].fields_by_name['encode_method']._serialized_options = b'\272H\013r\tR\007ordinal'
  _globals['_KBINSDISCRETIZER'].fields_by_name['strategy']._options = None
  _globals['_KBINSDISCRETIZER'].fields_by_name['strategy']._serialized_options = b'\272H\035r\033R\007uniformR\010quantileR\006kmeans'
  _globals['_NAMEDTABLES_TABLESENTRY']._options = None
  _globals['_NAMEDTABLES_TABLESENTRY']._serialized_options = b'8\001'
  _globals['_JOINTYPE']._serialized_start=13205
  _globals['_JOINTYPE']._serialized_end=13289
  _globals['_AGGREGATIONTYPE']._serialized_start=13292
  _globals['_AGGREGATIONTYPE']._serialized_end=13502
  _globals['_LOGICALCOMBINATION']._serialized_start=13504
  _globals['_LOGICALCOMBINATION']._serialized_end=13619
  _globals['_COMPARISONTYPE']._serialized_start=13622
  _globals['_COMPARISONTYPE']._serialized_end=13815
  _globals['_FLOATBITWIDTH']._serialized_start=13817
  _globals['_FLOATBITWIDTH']._serialized_end=13913
  _globals['_TABLECOMPUTEOP']._serialized_start=143
  _globals['_TABLECOMPUTEOP']._serialized_end=2652
  _globals['_JOINOP']._serialized_start=2655
  _globals['_JOINOP']._serialized_end=2926
  _globals['_RENAMECOLUMNSOP']._serialized_start=2929
  _globals['_RENAMECOLUMNSOP']._serialized_end=3159
  _globals['_RENAMECOLUMNSOP_OLDNAMESTONEWENTRY']._serialized_start=3095
  _globals['_RENAMECOLUMNSOP_OLDNAMESTONEWENTRY']._serialized_end=3159
  _globals['_TEXTFEATURETYPE']._serialized_start=3161
  _globals['_TEXTFEATURETYPE']._serialized_end=3178
  _globals['_CATEGORICALFEATURETYPE']._serialized_start=3180
  _globals['_CATEGORICALFEATURETYPE']._serialized_end=3204
  _globals['_PRIMARYKEYFEATURETYPE']._serialized_start=3206
  _globals['_PRIMARYKEYFEATURETYPE']._serialized_end=3229
  _globals['_FOREIGNKEYFEATURETYPE']._serialized_start=3231
  _globals['_FOREIGNKEYFEATURETYPE']._serialized_end=3304
  _globals['_IDENTIFIERFEATURETYPE']._serialized_start=3306
  _globals['_IDENTIFIERFEATURETYPE']._serialized_end=3329
  _globals['_NUMERICALFEATURETYPE']._serialized_start=3331
  _globals['_NUMERICALFEATURETYPE']._serialized_end=3353
  _globals['_MULTICATEGORICALFEATURETYPE']._serialized_start=3355
  _globals['_MULTICATEGORICALFEATURETYPE']._serialized_end=3384
  _globals['_TIMESTAMPFEATURETYPE']._serialized_start=3386
  _globals['_TIMESTAMPFEATURETYPE']._serialized_end=3408
  _globals['_EMBEDDINGFEATURETYPE']._serialized_start=3410
  _globals['_EMBEDDINGFEATURETYPE']._serialized_end=3432
  _globals['_UNKNOWNFEATURETYPE']._serialized_start=3434
  _globals['_UNKNOWNFEATURETYPE']._serialized_end=3454
  _globals['_FEATURETYPE']._serialized_start=3457
  _globals['_FEATURETYPE']._serialized_end=4222
  _globals['_SELECTFROMSTAGINGOP']._serialized_start=4225
  _globals['_SELECTFROMSTAGINGOP']._serialized_end=4429
  _globals['_SELECTCOLUMNSOP']._serialized_start=4431
  _globals['_SELECTCOLUMNSOP']._serialized_end=4529
  _globals['_LIMITROWSOP']._serialized_start=4531
  _globals['_LIMITROWSOP']._serialized_end=4626
  _globals['_ORDERBYOP']._serialized_start=4628
  _globals['_ORDERBYOP']._serialized_end=4740
  _globals['_FILTERROWSOP']._serialized_start=4742
  _globals['_FILTERROWSOP']._serialized_end=4868
  _globals['_DISTINCTROWSOP']._serialized_start=4870
  _globals['_DISTINCTROWSOP']._serialized_end=4941
  _globals['_UPDATEMETADATAOP']._serialized_start=4944
  _globals['_UPDATEMETADATAOP']._serialized_end=5085
  _globals['_SETMETADATAOP']._serialized_start=5088
  _globals['_SETMETADATAOP']._serialized_end=5218
  _globals['_REMOVEFROMMETADATAOP']._serialized_start=5220
  _globals['_REMOVEFROMMETADATAOP']._serialized_end=5335
  _globals['_UPDATEFEATURETYPESOP']._serialized_start=5338
  _globals['_UPDATEFEATURETYPESOP']._serialized_end=5613
  _globals['_UPDATEFEATURETYPESOP_NEWFEATURETYPESENTRY']._serialized_start=5519
  _globals['_UPDATEFEATURETYPESOP_NEWFEATURETYPESENTRY']._serialized_end=5613
  _globals['_ROLLUPBYAGGREGATIONOP']._serialized_start=5616
  _globals['_ROLLUPBYAGGREGATIONOP']._serialized_end=5866
  _globals['_COMBINEFILTERSROWFILTER']._serialized_start=5869
  _globals['_COMBINEFILTERSROWFILTER']._serialized_end=6037
  _globals['_COMPARECOLUMNTOLITERALROWFILTER']._serialized_start=6040
  _globals['_COMPARECOLUMNTOLITERALROWFILTER']._serialized_end=6228
  _globals['_ROWFILTER']._serialized_start=6231
  _globals['_ROWFILTER']._serialized_end=6444
  _globals['_EMPTYOP']._serialized_start=6446
  _globals['_EMPTYOP']._serialized_end=6455
  _globals['_EDGELISTTABLE']._serialized_start=6458
  _globals['_EDGELISTTABLE']._serialized_end=6694
  _globals['_EMBEDNODE2VECFROMEDGELISTSOP']._serialized_start=6697
  _globals['_EMBEDNODE2VECFROMEDGELISTSOP']._serialized_end=6895
  _globals['_EMBEDDINGMETRICSOP']._serialized_start=6897
  _globals['_EMBEDDINGMETRICSOP']._serialized_end=7022
  _globals['_EMBEDDINGCOORDINATESOP']._serialized_start=7025
  _globals['_EMBEDDINGCOORDINATESOP']._serialized_end=7239
  _globals['_READFROMPARQUETOP']._serialized_start=7242
  _globals['_READFROMPARQUETOP']._serialized_end=7429
  _globals['_SELECTFROMVECTORSTAGINGOP']._serialized_start=7432
  _globals['_SELECTFROMVECTORSTAGINGOP']._serialized_end=7798
  _globals['_CONCATOP']._serialized_start=7801
  _globals['_CONCATOP']._serialized_end=7969
  _globals['_UNNESTSTRUCTOP']._serialized_start=7971
  _globals['_UNNESTSTRUCTOP']._serialized_end=8088
  _globals['_NESTINTOSTRUCTOP']._serialized_start=8091
  _globals['_NESTINTOSTRUCTOP']._serialized_end=8259
  _globals['_ADDLITERALCOLUMNOP']._serialized_start=8262
  _globals['_ADDLITERALCOLUMNOP']._serialized_end=8567
  _globals['_CONCATSTRING']._serialized_start=8569
  _globals['_CONCATSTRING']._serialized_end=8613
  _globals['_CONCATLIST']._serialized_start=8615
  _globals['_CONCATLIST']._serialized_end=8627
  _globals['_COMBINECOLUMNSOP']._serialized_start=8630
  _globals['_COMBINECOLUMNSOP']._serialized_end=8931
  _globals['_ONEHOTENCODER']._serialized_start=8933
  _globals['_ONEHOTENCODER']._serialized_end=8948
  _globals['_MINMAXSCALER']._serialized_start=8950
  _globals['_MINMAXSCALER']._serialized_end=9052
  _globals['_LABELBINARIZER']._serialized_start=9054
  _globals['_LABELBINARIZER']._serialized_end=9128
  _globals['_LABELENCODER']._serialized_start=9130
  _globals['_LABELENCODER']._serialized_end=9144
  _globals['_KBINSDISCRETIZER']._serialized_start=9147
  _globals['_KBINSDISCRETIZER']._serialized_end=9312
  _globals['_BINARIZER']._serialized_start=9314
  _globals['_BINARIZER']._serialized_end=9355
  _globals['_MAXABSSCALER']._serialized_start=9357
  _globals['_MAXABSSCALER']._serialized_end=9371
  _globals['_STANDARDSCALER']._serialized_start=9373
  _globals['_STANDARDSCALER']._serialized_end=9445
  _globals['_ENCODER']._serialized_start=9448
  _globals['_ENCODER']._serialized_end=10033
  _globals['_ENCODECOLUMNOP']._serialized_start=10036
  _globals['_ENCODECOLUMNOP']._serialized_end=10238
  _globals['_EMBEDCOLUMNOP']._serialized_start=10241
  _globals['_EMBEDCOLUMNOP']._serialized_end=10616
  _globals['_MIN']._serialized_start=10618
  _globals['_MIN']._serialized_end=10623
  _globals['_MAX']._serialized_start=10625
  _globals['_MAX']._serialized_end=10630
  _globals['_MEAN']._serialized_start=10632
  _globals['_MEAN']._serialized_end=10638
  _globals['_STD']._serialized_start=10640
  _globals['_STD']._serialized_end=10645
  _globals['_QUANTILE']._serialized_start=10647
  _globals['_QUANTILE']._serialized_end=10685
  _globals['_COUNT']._serialized_start=10687
  _globals['_COUNT']._serialized_end=10694
  _globals['_NULLCOUNT']._serialized_start=10696
  _globals['_NULLCOUNT']._serialized_end=10707
  _globals['_AGGREGATION']._serialized_start=10710
  _globals['_AGGREGATION']._serialized_end=11061
  _globals['_AGGREGATECOLUMNSOP']._serialized_start=11064
  _globals['_AGGREGATECOLUMNSOP']._serialized_end=11236
  _globals['_CORRELATECOLUMNSOP']._serialized_start=11238
  _globals['_CORRELATECOLUMNSOP']._serialized_end=11348
  _globals['_HISTOGRAMCOLUMNOP']._serialized_start=11351
  _globals['_HISTOGRAMCOLUMNOP']._serialized_end=11556
  _globals['_ADDROWINDEXOP']._serialized_start=11559
  _globals['_ADDROWINDEXOP']._serialized_end=11704
  _globals['_CONVERTCOLUMNTOSTRINGOP']._serialized_start=11706
  _globals['_CONVERTCOLUMNTOSTRINGOP']._serialized_end=11819
  _globals['_OUTPUTCSVOP']._serialized_start=11822
  _globals['_OUTPUTCSVOP']._serialized_end=11954
  _globals['_TRUNCATELISTOP']._serialized_start=11957
  _globals['_TRUNCATELISTOP']._serialized_end=12181
  _globals['_TABLESLICEARGS']._serialized_start=12183
  _globals['_TABLESLICEARGS']._serialized_end=12247
  _globals['_TABLECOMPUTECONTEXT']._serialized_start=12250
  _globals['_TABLECOMPUTECONTEXT']._serialized_end=12481
  _globals['_TABLECOMPUTERESULT']._serialized_start=12483
  _globals['_TABLECOMPUTERESULT']._serialized_end=12587
  _globals['_EXECUTEREQUEST']._serialized_start=12590
  _globals['_EXECUTEREQUEST']._serialized_end=12724
  _globals['_EXECUTERESPONSE']._serialized_start=12726
  _globals['_EXECUTERESPONSE']._serialized_end=12834
  _globals['_STREAMEXECUTEREQUEST']._serialized_start=12836
  _globals['_STREAMEXECUTEREQUEST']._serialized_end=12936
  _globals['_STREAMEXECUTERESPONSE']._serialized_start=12938
  _globals['_STREAMEXECUTERESPONSE']._serialized_end=13033
  _globals['_NAMEDTABLES']._serialized_start=13036
  _globals['_NAMEDTABLES']._serialized_end=13203
  _globals['_NAMEDTABLES_TABLESENTRY']._serialized_start=13115
  _globals['_NAMEDTABLES_TABLESENTRY']._serialized_end=13203
  _globals['_TABLECOMPUTESERVICE']._serialized_start=13916
  _globals['_TABLECOMPUTESERVICE']._serialized_end=14109
# @@protoc_insertion_point(module_scope)
