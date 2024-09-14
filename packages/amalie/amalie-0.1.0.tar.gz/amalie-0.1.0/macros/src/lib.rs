extern crate proc_macro;
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, Expr, ExprLit, Lit, visit_mut::VisitMut, ExprArray, Token};
use syn::parse::{Parse, ParseStream};

#[proc_macro]
pub fn zz(input: TokenStream) -> TokenStream {
    let mut ast = parse_macro_input!(input as Expr);
    ZZTransformer.visit_expr_mut(&mut ast);
    TokenStream::from(quote! { #ast })
}


struct ZZTransformer;

impl VisitMut for ZZTransformer {
    fn visit_expr_mut(&mut self, node: &mut Expr) {
        match node {
            Expr::Lit(ExprLit { lit: Lit::Int(lit_int), .. }) => {
                let value = lit_int.base10_digits();
                if value == "1" {
                    *node = syn::parse_quote! {
                       ZZ::one()
                    };
                }
                else if value == "0" {
                    *node = syn::parse_quote! {
                       ZZ::zero()
                    };
                }
                else {
                    *node = syn::parse_quote! {
                       ZZ::zz_from_str(#value).unwrap()
                    };
                }
            },
            _ => syn::visit_mut::visit_expr_mut(self, node),
        }
    }
}

struct VecZZInput {
    values: Vec<Expr>,
}

impl Parse for VecZZInput {
    fn parse(input: ParseStream) -> syn::Result<Self> {
        let mut values = Vec::new();
        while !input.is_empty() {
            let value: Expr = input.parse()?;
            if !input.is_empty() {
                let _: Token![,] = input.parse()?;
            }
            values.push(value);
        }
        Ok(VecZZInput { values })
    }
}

#[proc_macro]
pub fn vec_zz(input: TokenStream) -> TokenStream {
    let VecZZInput { mut values } = parse_macro_input!(input as VecZZInput);

    let vector = values.iter_mut().map(|value| {
        quote! {
            zz!(#value)
        }
    });

    let output = quote! {
        vec![#(#vector),*]
    };
    output.into()
}

struct MatrixInput {
    rows: Vec<ExprArray>,
}

impl Parse for MatrixInput {
    fn parse(input: ParseStream) -> syn::Result<Self> {
        let mut rows = Vec::new();
        while !input.is_empty() {
            let row: ExprArray = input.parse()?;
            if !input.is_empty() {
                let _: Token![,] = input.parse()?;
            }
            rows.push(row);
        }
        Ok(MatrixInput { rows })
    }
}

#[proc_macro]
pub fn matrix(input: TokenStream) -> TokenStream {
    let MatrixInput { mut rows } = parse_macro_input!(input as MatrixInput);

    let matrix = rows.iter_mut().map(|row| {
        let elements = row.elems.iter_mut().map(|mut num| {
            ZZTransformer.visit_expr_mut(&mut num);
            quote! {
                #num
            }
        });
        quote! {
            vec![#(#elements),*]
        }
    });

    let output = quote! {
        {
            let m: Matrix = vec![#(zz!(#matrix)),*].try_into().unwrap(); 
            m 
        }
    };
    output.into()
}

