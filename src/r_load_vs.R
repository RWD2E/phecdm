cdm_code_type_map<-function(cdtype){
  if(grepl("icd9",tolower(cdtype))){
    return("09")
  }else if(grepl("icd10",tolower(cdtype))){
    return("10")
  }else if(grepl("loinc",tolower(cdtype))){
    return("LC")
  }else if(grepl("rxn",tolower(cdtype))){
    return("RX")
  }else if(grepl("ndc",tolower(cdtype))){
    return("ND")
  }else if(grepl("snom",tolower(cdtype))){
    return("SM")
  }else if(grepl("hcpcs",tolower(cdtype))){
    return("CH")
  }else if(grepl("cpt",tolower(cdtype))){
    return("CH")
  }else{
    stop("Standardized value doesn't exist for code type:",cdtype)
  }
}

load_valueset.ncbo<-function(
  vs_url = "",
  vs_name_str = ""
){
  # load valueset in json
  vs_file_type<-gsub(".*\\.","=",vs_url)
  vs_file<-jsonlite::fromJSON(vs_url)
  
  # initialize lookup table
  lookup_tbl<-data.frame(
    CODE_TYPE=as.character(),
    CODE_TYPE_CDM=as.character(),
    CODE_SUBTYPE=as.character(),
    CODE=as.character(),
    CODE_GRP=as.character(),
    stringsAsFactors=F
    )
  
  # main code body for parsing json file
  vs_name_list<-names(vs_file)
  vs_name_dist<-stringdist(tolower(vs_name_str),vs_name_list, method="jw")
  vs_name_match<-vs_name_list[which.min(vs_name_dist)]
  vs<-vs_file[[vs_name_match]]
  for(cd_type_idx in seq_along(vs[["code_type"]])){
    # skip if empty
    if(length(vs[["code_list"]])==0) next
    lookup_tbl %<>%
      bind_rows(data.frame(CODE_TYPE=vs[["code_type"]][[cd_type_idx]],
                           CODE_TYPE_CDM=cdm_code_type_map(vs[["code_type"]][cd_type_idx]),
                           CODE_SUBTYPE="exact",
                           CODE=vs[["code_list"]][[cd_type_idx]][["code"]],
                           CODE_GRP=vs_name_match,
                           stringsAsFactors = F))
  }
  # return data.frame   
  return(lookup_tbl)
}

load_valueset.rxnav<-function(
  vs_url = "",
  vs_name_str = ""
){
  # load valueset in json
  vs_file_type<-gsub(".*\\.","=",vs_url)
  vs_file<-jsonlite::fromJSON(vs_url)
  
  # initialize lookup table
  lookup_tbl<-data.frame(RXCUI=as.character(),
                         LABEL=as.character(),
                         NDC=as.character(),
                         stringsAsFactors=F)
  
  # main code body for parsing json file
  vs_name_list<-names(vs_file)
  vs_name_dist<-stringdist(tolower(vs_name_str),vs_name_list, method="jw")
  vs_name_match<-vs_name_list[which.min(vs_name_dist)]
  vs<-vs_file[[vs_name_match]] %>% 
    filter(ndc!="character(0)") %>%
    unnest_wider(ndc,names_sep="_") %>%
    gather(ndc_idx,ndc,-rxcui,-label) %>%
    filter(!is.na(ndc)) %>% select(-ndc_idx)

  # return data.frame
  colnames(vs)<-toupper(colnames(vs))
  lookup_tbl %<>% bind_rows(data.frame(vs))
  return(lookup_tbl)
}

load_valueset.curated<-function(
  vs_url = "",
  vs_name_str = "",
  add_meta = FALSE
){
  # load valueset in json
  vs_file_type<-gsub(".*\\.","=",vs_url)
  vs_file<-jsonlite::fromJSON(vs_url)
  
  # initialize lookup table
  lookup_tbl<-data.frame(
    CODE_TYPE=as.character(),
    CODE_TYPE_CDM=as.character(),
    CODE=as.character(),
    CODE_GRP=as.character(),
    stringsAsFactors=F
  )
  if(add_meta){
    meta_tbl<-c()
  }

  # search closest concept key
  vs_name_list<-names(vs_file)
  if(vs_name_str != ""){
    vs_name_dist<-stringdist(tolower(vs_name_str),vs_name_list, method="jw")
    vs_name_match<-vs_name_list[which.min(vs_name_dist)]
  }else{
    vs_name_match<-vs_name_list
  }

  for(key in vs_name_match){
    vs<-vs_file[[key]]
    if(add_meta){
      # metadata
      meta_tbl %<>% 
        bind_rows(
          cbind(
            CODE_GRP=key,
            as.data.frame(do.call(cbind, vs[["meta"]]))
          )
        )
    }

    # valuesets
    for(cd_type in names(vs)){
      if(cd_type == "meta") next
      # exact list without decimal points
      cd_lst<-vs[[cd_type]] 
      # stack up
      lookup_tbl %<>%
        bind_rows(data.frame(
          CODE_TYPE=cd_type,
          CODE_TYPE_CDM=cdm_code_type_map(cd_type),
          CODE=as.character(cd_lst),
          CODE_GRP=key,
          stringsAsFactors = F
        ))
    }
  }
  
  # return data.frame
  out<-lookup_tbl %>% 
    inner_join(meta_tbl,by="CODE_GRP")
  return(out)
}

load_valueset.ecqm<-function(
  vs_url = "",
  vs_name_str = ""
){
  # load valueset in json
  vs_file_type<-gsub(".*\\.","=",vs_url)
  vs_file<-jsonlite::fromJSON(vs_url)
  
  # initialize lookup table
  lookup_tbl<-data.frame(CODE_TYPE=as.character(),
                         CODE_TYPE_CDM=as.character(),
                         CODE_SUBTYPE=as.character(),
                         CODE=as.character(),
                         CODE_GRP=as.character(),
                         stringsAsFactors=F)
  
  # main code body for parsing json file
  vs_name_list<-names(vs_file)
  vs_name_dist<-stringdist(tolower(vs_name_str),vs_name_list, method="jw")
  vs_name_match<-vs_name_list[which.min(vs_name_dist)]
  vs<-vs_file[[vs_name_match]]
  for(cd_type in names(vs[["codelist"]])){
    cd_lst<-vs[["codelist"]][[cd_type]][,1]
    lookup_tbl %<>%
      bind_rows(data.frame(CODE_TYPE=cd_type,
                           CODE_TYPE_CDM=cdm_code_type_map(cd_type),
                           CODE_SUBTYPE="exact",
                           CODE=as.character(cd_lst),
                           CODE_GRP=vs_name_match,
                           stringsAsFactors = F))
    }
  # return data.frame
  return(lookup_tbl)
}

load_valueset.vsac<-function(
  vs_url = "",
  vs_name_str = ""
){
  # load valueset in json
  vs_file_type<-gsub(".*\\.","=",vs_url)
  lookup_tbl<-jsonlite::fromJSON(vs_url) %>%
    unnest(vs) %>%
    rename(
      "CODEGRP" = "oid" ,
      "CODEGRP_LABEL" = "displayName",
      "CODE" = "@code",
      "CODE_LABEL" = "@displayName",
      "CODE_TYPE" = "@codeSystemName"
    ) %>%
    mutate(CODE_TYPE_CDM = unlist(lapply(CODE_TYPE, function(x) cdm_code_type_map(x)))) %>%
    select(CODE_TYPE,CODE_TYPE_CDM,CODE,CODE_LABEL,CODEGRP,CODEGRP_LABEL) 

  # return data.frame
  return(lookup_tbl)
}

load_valueset<-function(
  vs_template = c("curated",
                  "ecqm",
                  "ncbo",
                  "rxnav",
                  "vsac"),
  vs_url = "",
  vs_name_str = "",
  add_meta = TRUE,
  dry_run = TRUE,
  conn=NULL,
  write_to_schema = "PUBLIC",
  write_to_tbl = "TEMP",
  overwrite=TRUE,
  file_encoding ="latin-1"
){
  vs_load_func<-get(paste0("load_valueset.",vs_template))
  if(vs_template=="curated"){
    lookup_tbl<-vs_load_func(vs_url=vs_url,vs_name_str=vs_name_str,add_meta = add_meta)
  }else{
    lookup_tbl<-vs_load_func(vs_url=vs_url,vs_name_str=vs_name_str)
  }
  
  # run query
  if(dry_run==TRUE){
    return(lookup_tbl)
  }else{
    if(is.null(conn)){
      stop("connection needs to be specified!")
    }else{
      # specify field.types to accommodate long strings
      max_str<-rep("varchar(500)",ncol(lookup_tbl))
      names(max_str) <- names(lookup_tbl)
      if(!overwrite){
        max_str = NULL
      }
      # write valueset table to target db
      DBI::dbWriteTable(
        conn,
        SQL(paste0(write_to_schema,".",write_to_tbl)),
        lookup_tbl,
        overwrite = overwrite,
        append = !overwrite,
        file_encoding = file_encoding,
        field.types = max_str
      )
    }
  }
}