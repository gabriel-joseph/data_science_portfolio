# .Rprofile
setHook("rstudio.onSave", function(...) {
  styler::style_active_file()
})

styler::style_file("script.R", strict = TRUE)

